# typecast-api-mcp-server-sample

MCP Server for typecast-api, enabling seamless integration with MCP clients. This project provides a standardized way to interact with Typecast API through the Model Context Protocol.

## About

이 프로젝트는 Typecast API를 위한 Model Context Protocol 서버를 구현하여, MCP 클라이언트가 표준화된 방식으로 Typecast API와 상호작용할 수 있도록 합니다.

## Feature Implementation Status

| Feature              | Status |
| -------------------- | ------ |
| **Voice Management** |        |
| Get Voices           | ✅     |
| Text to Speech       | ✅     |
| Play Audio           | ✅     |

## Setup

### Dependencies

이 프로젝트는 Python 3.10 이상이 필요하며, `uv`를 사용하여 패키지를 관리합니다.

#### 패키지 설치

```bash
# 가상 환경 생성 및 패키지 설치
uv venv
uv pip install -e .

```

### Environment Variables

다음 환경 변수를 설정하세요:

```bash
TYPECAST_API_HOST=https://api.typecast.ai
TYPECAST_API_KEY=<your-api-key>
TYPECAST_OUTPUT_DIR=<your-output-directory> # default: ~/Downloads/typecast_output
```

### Usage with Claude Desktop

`claude_desktop_config.json`에 다음과 같이 추가할 수 있습니다:

#### 기본 설정:

```json
{
  "mcpServers": {
    "typecast-api-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/PATH/TO/YOUR/PROJECT",
        "run",
        "typecast-api-mcp-server"
      ],
      "env": {
        "TYPECAST_API_HOST": "https://api.typecast.ai",
        "TYPECAST_API_KEY": "YOUR_API_KEY",
        "TYPECAST_OUTPUT_DIR": "PATH/TO/YOUR/OUTPUT/DIR"
      }
    }
  }
}
```

`/PATH/TO/YOUR/PROJECT`를 실제 프로젝트가 위치한 경로로 변경하세요.

### Manual Execution

서버를 수동으로 실행할 수도 있습니다:

```bash
uv run python app/main.py
```

## Contributing

기여는 언제나 환영합니다! Pull Request를 자유롭게 제출해주세요.

## License

MIT License
