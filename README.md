# korea-transit-planner

[![CI](https://github.com/bohe76/korea-transit-planner-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/bohe76/korea-transit-planner-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-111111.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-0066cc.svg)](CHANGELOG.md)

출발지부터 목적지 문 앞까지, 한국 대중교통을 같은 시간 기준으로 비교하는 에이전트 스킬입니다.

`korea-transit-planner`는 일반 지하철, 시내·시외버스, 마을버스, 누리버스/DRT, 도보, 택시, 혼합 경로를 조사할 때 쓰는 재사용 가능한 절차입니다. 지도 서비스의 후보 경로와 공식 운행·운임 정보를 구분하고, 첫·마지막 구간과 대기·환승까지 포함합니다.

> 이 저장소는 라우팅 엔진이나 교통 데이터셋이 아닙니다. API 키, 비공개 주소, 개인 캘린더 정보, 지도 타일을 포함하지 않습니다.

English overview: [README.en.md](README.en.md)

## 핵심 원칙

- 출발지는 반드시 사용자가 명시합니다. 저장된 집 주소나 개인 기본값을 추정하지 않습니다.
- 사용자가 지정한 승·하차역은 제약 조건입니다. 같은 이름의 시설과 역을 구분합니다.
- 모든 후보는 동일한 출발/도착 시각 기준으로 문 앞부터 문 앞까지 비교합니다.
- 공식 운영사·공공 데이터를 시간표와 운임의 우선 근거로 사용합니다.
- 실시간 정보에는 조회 시각과 시간대를 붙이고, 추정치는 추정치라고 표시합니다.
- GTX는 사용자가 `GTX`를 직접 언급하거나 GTX 역명을 지정한 경우에만 조회·비교합니다.

## 다루는 이동수단

| 이동수단 | 비교 포인트 |
|---|---|
| 일반 지하철 | 승강장 접근, 배차, 환승, 출구, 도보 |
| 시내·시외버스 | 정류장 접근, 배차, 정체, 환승, 운임 |
| 마을버스 | 지역 운영 주체, 정류장, 운행일·배차 |
| 누리버스/DRT | 서비스 구역, 예약, 운영시간, 탑승 조건 |
| 도보 | 실제 보행 구간, 경사·접근성, 환승 연결 |
| 택시 | 교통량, 호출 대기, 요금 신뢰도, 승하차 지점 |
| 혼합 경로 | 각 구간의 연결성과 전체 문전 시간 |

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

## 사용 예

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

응답 구조 예시: [examples/route-briefing.md](korea-transit-planner/examples/route-briefing.md)

## 데이터와 검증

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

검증기는 구조, 프런트매터, 명시 출발지 우선순위, GTX 옵트인 계약, 필수 이동수단, 비공개 문자열·시크릿 패턴을 확인합니다. GitHub Actions에서도 같은 명령을 실행합니다.

## 개인정보·보안

공개 코어에는 개인 출발지, 캘린더 정체성, 계정 식별자, API 키를 넣지 않습니다. 취약점이나 비공개 유출 가능성은 공개 이슈에 민감한 값을 붙이지 말고 [SECURITY.md](SECURITY.md)의 절차를 따르세요.

## 기여

작은 문서 수정부터 새로운 지역 운영사 출처 추가까지 환영합니다. [CONTRIBUTING.md](CONTRIBUTING.md)를 확인하세요. 실제 사용에서 얻은 개선은 일반화하고 개인정보를 제거한 뒤 SemVer로 배포할 수 있습니다.

## 라이선스

[MIT](LICENSE)
