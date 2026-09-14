# korea-transit-planner

[![CI](https://github.com/bohe76/korea-transit-planner-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/bohe76/korea-transit-planner-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-111111.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-0066cc.svg)](CHANGELOG.md)

<img src="docs/assets/korea-transit-planner-hero.svg" alt="korea-transit-planner: explicit origin, same-time comparison, verified sources" width="100%" />

한국 대중교통을 출발지부터 목적지 문 앞까지, **같은 도착 시각 기준**으로 비교하는 한국어 우선 에이전트 스킬입니다.

`korea-transit-planner`는 지하철·버스·마을버스·누리버스/DRT·도보·택시·혼합 경로를 조사하는 재사용 가능한 절차입니다. 지도 서비스는 후보를 찾는 데 쓰고, 시간표와 운임은 공식 운영사·공공 출처로 다시 확인합니다.

> **절차 스킬입니다.** 라우팅 엔진·교통 데이터셋·API 키·비공개 주소·개인 캘린더·지도 타일을 포함하지 않습니다.

English overview: [README.en.md](README.en.md)

| 바로가기 | 내용 |
|---|---|
| [빠른 설치](#빠른-설치--hermes-agent) | Hermes Agent에서 검토 후 설치 |
| [요청 예시](#요청-예시) | 일반 이동수단과 GTX 옵트인 요청 |
| [검증 방식](#출처와-검증-방식) | 후보·공식 근거·불확실성의 구분 |
| [개인정보·보안](#개인정보보안) | 공개 코어의 데이터 경계 |
| [기여](#기여) | 출처·프라이버시를 지키는 개선 |

## 무엇을 비교하나요

| 이동수단 | 비교에 포함하는 항목 |
|---|---|
| 일반 지하철 | 승강장 접근, 배차, 환승, 출구, 도보 |
| 시내·시외버스 | 정류장 접근, 배차, 정체, 환승, 운임 |
| 마을버스 | 지역 운영 주체, 정류장, 운행일·배차 |
| 누리버스/DRT | 서비스 구역, 예약, 운영시간, 탑승 조건 |
| 도보 | 실제 보행 구간, 경사·접근성, 환승 연결 |
| 택시 | 교통량, 호출 대기, 요금 신뢰도, 승하차 지점 |
| 혼합 경로 | 각 구간의 연결성과 전체 문전 시간 |

## 핵심 원칙

1. **명시한 출발지**만 사용합니다. 저장된 집 주소나 개인 기본값을 추정하지 않습니다.
2. 사용자가 지정한 승·하차역은 **제약 조건**입니다. 같은 이름의 시설과 역을 구분합니다.
3. 모든 후보를 **같은 출발·도착 시각 기준**으로 문 앞부터 문 앞까지 비교합니다.
4. 실시간 정보에는 조회 시각과 시간대를 붙이고, 추정치는 추정치라고 표시합니다.
5. **GTX는 옵트인**입니다. 사용자가 `GTX`를 직접 언급하거나 GTX 역명을 지정한 경우에만 조회·비교합니다.

## 빠른 설치 — Hermes Agent

먼저 내용을 검토하세요.

```bash
hermes skills inspect bohe76/korea-transit-planner-skill/korea-transit-planner
```

검토 후 설치합니다.

```bash
hermes skills install bohe76/korea-transit-planner-skill/korea-transit-planner
```

직접 URL 설치도 가능합니다.

```bash
hermes skills install https://raw.githubusercontent.com/bohe76/korea-transit-planner-skill/main/korea-transit-planner/SKILL.md
```

Hermes Agent 최신 스킬 문서: <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills>

## 다른 에이전트에서 사용

이 스킬은 `SKILL.md` 중심의 텍스트 절차입니다. 사용하는 런타임이 [Agent Skills 사양](https://agentskills.io/specification)과 로컬 참조 파일 로딩을 지원하는지 확인한 뒤 저장소를 복제하거나 해당 런타임의 설치 방식을 따르세요. 특정 런타임과의 호환성은 실제 검증 없이 보장하지 않습니다.

```bash
git clone https://github.com/bohe76/korea-transit-planner-skill.git
```

## 요청 예시

일반 경로는 출발지·목적지·도착 기준 시각·비교할 수단을 함께 명시합니다.

```text
출발지는 부산역, 목적지는 해운대해수욕장이야.
토요일 14:00 도착 기준으로 지하철·버스·택시를 비교해 줘.
첫 이동, 대기, 환승, 마지막 도보, 비용 신뢰도와 10분 여유를 포함해.
```

GTX를 비교하려면 명시적으로 요청합니다.

```text
출발지는 서울역, 목적지는 킨텍스 제1전시장이고 GTX-A 킨텍스역에서 내려야 해.
같은 도착 시각 기준으로 일반 지하철과 비교해 줘.
```

### 응답은 이렇게 읽습니다

결과는 추천 이유와 함께 `문전 소요시간`, `대기·환승`, `도보`, `운임/신뢰도`, `도착 위험`을 나란히 보여야 합니다. 현재 운행 사실과 지도 후보, 추정 범위를 분리하고 조회 시각을 남깁니다.

전체 형식은 [가상 경로 브리핑 예시](korea-transit-planner/examples/route-briefing.md)에서 확인할 수 있습니다. 예시에 현재 교통 데이터나 실제 개인 이동 정보는 없습니다.

## 출처와 검증 방식

| 정보 | 우선 근거 | 결과에 남기는 것 |
|---|---|---|
| 시간표·운임·운행 조건 | 공식 운영사 또는 공공 출처 | 출처와 확인 시각 |
| 경로 후보·보행 연결 | 지도 서비스 | 후보임을 표시하고 공식 정보로 교차 확인 |
| 정체·호출 대기 등 변동값 | 조회 가능한 현재 정보 | 조회 시각·시간대와 불확실성 |

세부 절차와 출처 경계:

- [지도 경로 후보 검증](korea-transit-planner/references/map-routing.md)
- [공식/보조 출처 우선순위](korea-transit-planner/references/source-verification.md)
- [GTX 옵트인 절차](korea-transit-planner/references/gtx-routing.md)
- [마을버스·누리버스·DRT 확인](korea-transit-planner/references/local-modes.md)

지도 서비스의 이용약관을 준수하세요. 이 저장소는 스크래핑한 독점 데이터나 지도 자산을 재배포하지 않습니다.

## 개발과 검증

Python 3.9 이상, 외부 패키지 없이 실행됩니다.

```bash
python scripts/validate.py .
python -m unittest discover -s tests -v
```

검증기는 구조·프런트매터·명시 출발지 우선순위·GTX 옵트인 계약·필수 이동수단·비공개 문자열 및 시크릿 패턴을 확인합니다. GitHub Actions에서도 같은 명령을 실행합니다.

## 개인정보·보안

공개 코어에는 개인 출발지, 캘린더 정체성, 계정 식별자, API 키를 넣지 않습니다. 실제 사용에서 얻은 개선은 일반화하고 개인정보를 제거한 뒤에만 제안하세요. 취약점이나 비공개 유출 가능성은 공개 이슈에 민감한 값을 붙이지 말고 [SECURITY.md](SECURITY.md)의 절차를 따르세요.

## 기여

작은 문서 수정부터 지역 운영사 출처 추가까지 환영합니다. [CONTRIBUTING.md](CONTRIBUTING.md)의 출처·개인정보·계약 체크리스트를 확인하고, 하나의 목적에 집중한 PR로 보내 주세요.

호환 가능한 일반화·개인정보 안전 개선은 SemVer에 따라 배포할 수 있습니다. 출발지, GTX, 역 제약, 개인정보 또는 출력 계약을 깨는 변경은 메이저 버전으로 다룹니다. 모든 릴리스에는 관리자의 검토가 필요하며 자동 릴리스는 하지 않습니다.

## 라이선스

[MIT](LICENSE)
