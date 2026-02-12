[![Build](https://github.com/azhezyz/2AA4_Bonus2/actions/workflows/build.yml/badge.svg)](https://github.com/azhezyz/2AA4_Bonus2/actions/workflows/build.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=azhezyz_2AA4_Bonus2&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=azhezyz_2AA4_Bonus2)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=azhezyz_2AA4_Bonus2&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=azhezyz_2AA4_Bonus2)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=azhezyz_2AA4_Bonus2&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=azhezyz_2AA4_Bonus2)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=azhezyz_2AA4_Bonus2&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=azhezyz_2AA4_Bonus2)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=azhezyz_2AA4_Bonus2&metric=coverage)](https://sonarcloud.io/summary/new_code?id=azhezyz_2AA4_Bonus2)
 # STARFORGE PROTOCOL: draw.io -> Python Codegen

[English](#english) | [中文](#中文)

## English

> Vessel ID: `codegen_poc`
>
> Mission: transform simplified draw.io UML signals into executable Python class stubs.

### What This Is

`drawio_codegen.py` parses a simplified draw.io (mxGraph XML) model and emits Python dataclasses.

Generated output includes:
- one file per class
- typed attributes for associations
- helper methods for `N`-cardinality links (`add_*`, `remove_*`)
- inheritance wiring

### Launch Sequence

Run from `codegen_poc/`:

```bash
python drawio_codegen.py examples/default/model/model.drawio examples/default/src_gen
python examples/default/client.py

python drawio_codegen.py examples/library/model/library.drawio.xml examples/library/src_gen
python examples/library/client.py
```

### Signal Format (Model Rules)

Association edge labels must follow:
- `name (1)`
- `name (N)`

Examples:
- `drives (1)`
- `hasWheel (N)`

Inheritance is detected when edge style contains:
- `endArrow=block`
- `endFill=0`

### Naming + Import Safety

The generator enforces stable field names and import-safe typing:
- normalizes role names to avoid accidental double underscores
- uses forward references for association types to avoid circular import crashes in bidirectional links

### Output Topology

Typical generated package:

```text
src_gen/
  __init__.py
  person.py
  car.py
  wheel.py
  ...
```

### Known Scope (PoC)

This is intentionally limited:
- assumes a simplified draw.io structure
- ignores edges with unparseable labels
- does not generate persistence, validation, or runtime graph constraints

### If The Reactor Fails

Quick checks:
1. confirm edge labels exactly match `name (1|N)`
2. confirm class nodes are `mxCell` with `vertex="1"`
3. regenerate into a clean output folder
4. run client with the same Python interpreter used for generation

### Coverage Uplink

To add test coverage into the build pipeline, this project uses:
- `tox` for test orchestration
- `pytest` for test execution
- `pytest-cov` / Coverage.py for coverage measurement

Run:

```bash
tox
```

Equivalent direct command:

```bash
pytest --cov=codegen_poc --cov-report=term-missing --cov-report=xml --cov-config=tox.ini --cov-branch
```

Artifacts:
- `coverage.xml` for CI upload/integration
- terminal missing-lines report for local debugging

## 中文

> 项目代号：`codegen_poc`
>
> 目标：将简化版 draw.io UML 信号转换为可执行的 Python 类骨架代码。

### 项目简介

`drawio_codegen.py` 会解析简化版 draw.io（mxGraph XML）模型并生成 Python dataclass。

生成结果包括：
- 每个类一个文件
- 关联关系的类型化属性
- `N` 基数关系的辅助方法（`add_*`、`remove_*`）
- 继承关系连接

### 快速运行

在 `codegen_poc/` 目录下执行：

```bash
python drawio_codegen.py examples/default/model/model.drawio examples/default/src_gen
python examples/default/client.py

python drawio_codegen.py examples/library/model/library.drawio.xml examples/library/src_gen
python examples/library/client.py
```

### 模型规则（信号格式）

关联边标签必须满足：
- `name (1)`
- `name (N)`

示例：
- `drives (1)`
- `hasWheel (N)`

当边样式包含以下内容时，会识别为继承关系：
- `endArrow=block`
- `endFill=0`

### 命名与导入安全

生成器会保证字段命名稳定和导入安全：
- 规范化 role 名称，避免意外双下划线
- 为关联类型使用前向引用，避免双向关系导致循环导入崩溃

### 输出结构

典型生成目录：

```text
src_gen/
  __init__.py
  person.py
  car.py
  wheel.py
  ...
```

### 当前范围（PoC）

当前实现有意保持精简：
- 假设输入为简化版 draw.io 结构
- 忽略无法解析标签的边
- 不生成持久化、校验或运行时图约束

### 故障排查

快速检查：
1. 确认边标签严格匹配 `name (1|N)`
2. 确认类节点是 `mxCell` 且 `vertex="1"`
3. 在干净输出目录中重新生成
4. 使用与生成阶段相同的 Python 解释器运行 client

### 覆盖率

项目使用以下工具接入测试覆盖率：
- `tox`：测试编排
- `pytest`：测试执行
- `pytest-cov` / Coverage.py：覆盖率统计

执行：

```bash
tox
```

等价命令：

```bash
pytest --cov=codegen_poc --cov-report=term-missing --cov-report=xml --cov-config=tox.ini --cov-branch
```

产物：
- `coverage.xml`：用于 CI 上传/集成
- 终端 missing-lines 报告：用于本地排查

