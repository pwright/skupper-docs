# Documentation analysis

Two read-only analyzers live here:

- [IWE tree reports](iwe.md): structural inventory and counts using the existing Python/IWE tool.
- [Remark AST analysis](ast.md): section classifications, source lines, confidence, warnings, and candidate DITA elements. The default scope is `input/`, excluding `input/refdog/`.

See [the content architecture proposal](content-architecture.md) for the relationship between reader purpose, topic type, ownership, and publication placement across both trees.

See [the structure simplification report](report.md) for proposed source conventions and a validation workflow using both analyzers.

See [the Refdog report](refdog-report.md) for generator and source-model changes that could simplify DITA conversion of `input/refdog/`.

The DITA writer is deferred until the classifications have been reviewed against real documentation.
