# Content architecture across input and Refdog

`input/` is the publication input tree. `input/refdog/` is a collection within it whose content is largely produced through Refdog. That is a production distinction, not a division between explanatory documentation and reference information.

A clearer architecture would describe **reader purpose, topic type, source ownership, and publication placement separately**. Concepts belong in Refdog when they explain its object model; reference topics can remain elsewhere when they describe another product surface, such as Network Observer configuration. Neither case requires moving files merely to make directory names match topic types.

This proposal brings together [the input structure report](report.md), [the Refdog report](refdog-report.md), and a repository-wide review of aliases, generators, publication, and validation tooling. It does not change source files, generators, navigation, or analyzer behavior.

## What the current organization is doing

[The documentation home page](../input/index.md) already offers several ways into the material: understanding the model, using the CLI, declaring networks in YAML, exploring concepts, and looking up definitions. [The generated navigation](../mkdocs.yml) also groups content by activities such as Discover, Deploy, Configure, and Observe.

Meanwhile, Refdog organizes material around commands, API resources, concepts, and supporting topics. Its [Site concept](../input/refdog/concepts/site.md) explains relationships among sites, networks, platforms, workloads, and routers. That is explanatory material, even though it is published alongside generated API and CLI references. Rendering authored concept YAML through a generator does not make the explanation schema-derived.

Conversely, [Network Observer configuration](../input/console/configuration.md) is primarily a lookup page containing paths, types, defaults, and descriptions. It appears under Observe, outside Refdog, and also contains a persistent-storage procedure. The reference content is appropriate to the console collection; its embedded task is a separate composition issue.

The present folders therefore combine several legitimate organizing principles. The confusing part is treating any one of those principles as the topic's meaning.

## Four separate decisions

| Decision | Question | Example values |
| --- | --- | --- |
| Reader purpose | What is the reader trying to understand or accomplish? | Understand sites; link sites; configure persistence; look up a flag |
| Topic type | What kind of information does this topic deliver? | Concept, task, reference |
| Source ownership | Who owns the facts and how are they maintained? | Editorial prose; CLI export; CRD schema plus metadata; configuration reference maintained against a versioned source |
| Publication placement | Where should readers encounter it? | Discover, Configure, Observe, API reference, CLI reference, object-model concepts |

A fifth distinction concerns composition: a page can be a standalone topic, a collection/assembly, or a landing page. **Assembly describes how content is composed; it is not another semantic topic type.** This refines the earlier reports' suggestion of a single `topic_type` vocabulary containing `assembly`. A composed page can have multiple member topics with different types.

Directory location can provide a useful default for a content collection. It should not override a reviewed topic type or establish factual authority.

## Recommended responsibilities

| Collection or area | Primary responsibility | What it should link to rather than duplicate |
| --- | --- | --- |
| `overview/` | Introduce the product, architecture, and key decisions at a reader-friendly level | Detailed object relationships, exact flags and resource fields |
| Platform/workflow guides: `kube-cli/`, `kube-yaml/`, `system-cli/`, `system-yaml/` | Help readers complete goals in a particular environment | Canonical command syntax, field definitions, shared conceptual explanations |
| `console/` | Explain and operate Network Observer, including its own configuration reference | Shared Skupper concepts and API/CLI details owned elsewhere |
| `refdog/concepts/` | Explain the core object model and relationships in depth | Introductory journeys and environment-specific procedures |
| `refdog/commands/` | Provide authoritative, versioned command and option descriptions | End-to-end workflows involving several commands |
| `refdog/resources/` | Provide authoritative, versioned resource and field descriptions | Deployment recipes and broader operational guidance |
| `refdog/topics/` | Retain useful supporting topics with an identified purpose and owner | Equivalent topics already maintained in other collections |

These are proposed responsibilities, not a claim that every current page already meets them. In particular, supporting `topics/` should not become a permanent miscellaneous category without a review of its contents and inbound links.

A task may include a short explanation or example. A concept may include a small table. A reference may include usage examples. Split content when it has an independently useful purpose or a distinct maintenance owner, rather than classifying every paragraph into a separate topic.

## Decide ownership at the fact level

A single topic can combine several sources. For example, a resource reference can use a CRD for field types and required membership, plus authored metadata for examples and operational explanations. Its semantic type remains reference.

| Information | Proposed canonical owner |
| --- | --- |
| CLI syntax, arguments, flag types/defaults | Pinned CLI export or validated extraction from upstream CLI documentation |
| Resource field schema, required membership, declared defaults | Selected, pinned CRD version |
| Object-model explanations and diagrams | Reviewed concept source, currently including Refdog concept configuration |
| Steps for linking sites on a particular platform | The corresponding workflow topic |
| Network Observer configuration paths and defaults | Its versioned configuration source, once identified and verified |
| Navigation grouping and reading order | Publication configuration, not a topic's storage directory |

The inspected repository does not contain a matching chart values/schema file establishing authority for all the console configuration tables. Before generating that reference, identify and pin its actual upstream source. Do not route it through the CRD generator merely because both outputs are reference topics.

Keep concise definitions in task context where readers need them, but link to the canonical explanation. A beginner overview and a detailed Site concept can coexist if their depth and purpose are distinct. Do not deduplicate them solely because both mention sites.

## Apply the architecture to the two examples

### Refdog concepts

Retain the core object-model concepts as concepts, with editorial ownership, regardless of their generated Markdown location. Publish links to them from Discover, workflows, and relevant reference pages. There is no need to copy the same explanation into `overview/` or move every concept out of Refdog.

For [the Site concept](../input/refdog/concepts/site.md), the authoring source is [concept configuration](../refdog/config/concepts/site.yaml), including descriptions and figures. Its conversion path should preserve that authored structure. It should not be treated as a byproduct of the Site CRD.

Review overlap between introductory overview content and object-model content by reader question: “What does Skupper do?” and “How does a Site relate to a Platform and Network?” are different purposes. Merge only where topics actually answer the same question at the same depth for the same audience.

### Network Observer configuration

Keep the configuration reference in the console collection unless an independent publishing need justifies relocation. Give it a reference identity and an owner responsible for matching the supported configuration version.

Extract the persistent-storage instructions into a task if they are independently useful. Keep the table of persistence values in the reference, and link the task to it. Let the Observe collection present both as part of the same reader journey.

The task should explain prerequisites, actions, and verification. The reference should define values and constraints. Shared facts should have one maintained source, even if a small configuration example appears in both contexts.

This resolves the mixed-topic case without treating all reference material as Refdog output.

## A minimal shared content contract

Both authoring paths should produce a comparable catalog of content. Authored files can supply reviewed metadata; generated objects can supply the same information through their model export. Build the catalog from those sources rather than maintaining a second manual inventory of the same facts.

| Field | Meaning |
| --- | --- |
| `id` | Stable logical identity, independent of display title and output URL |
| `document_role` | Topic, assembly, or landing page |
| `topic_type` | Concept, task, or reference for a topic; not inferred from its directory |
| `collection` | Owning subject collection, such as object model, CLI, API resources, or console |
| `sources` | Authoring location, upstream revision/version, and any field-specific provenance |
| `owner` | Maintainer responsible for reviewing content and source changes |
| `applies_to` | Relevant platform and product/API/configuration version |
| `relationships` | Logical links to related concepts, tasks, references, and collection members |

An assembly record should identify its members and ordering; its member topics carry their own semantic types. Not every proposed field needs to be added on day one. Start with identity, document role, reviewed type, and source ownership for a small pilot. The current AST analyzer does not yet interpret this contract, and the IWE wrapper does not validate it.

Section roles remain separate from these topic fields. A task's `Procedure` section does not create a second task; an example block in a reference does not change the reference into a procedure. Use structural warnings to reveal conflicting or ambiguous organization rather than let a section label decide the entire file's type.

## Navigation and DITA composition

Use reader journeys for the main navigation, and provide lookup views for commands, resources, configuration, and terminology. A topic can appear in several views through its identity and relationships without several maintained copies.

For a future DITA publication, topic types should follow the reviewed content purpose, while maps express reading order and collection membership. Refdog's generation model can supply command/resource navigation, and editorial publication configuration can place selected concepts or references in task-oriented journeys. Generated content need not become a separate reader silo.

The word “Reference” in navigation needs a precise scope. Either make it a lookup hub with explicit CLI, API, and configuration entries, or label the narrower collections directly. Do not use it as the only label for a collection that also houses conceptual deep dives and operational guidance.

Preserve current URLs and anchors while piloting this model. Review [the job mapping](../skupper-job-mapping.csv) and [navigation generator](../python/generate-mkdocs-nav.py) before changing paths or composition; navigation is already derived from more than folder names.

## What validation should establish

- **Purpose and ownership:** each reviewed topic has an identifiable reader question and maintained source; duplicates are assessed by purpose, not vocabulary overlap.
- **Structure:** task sections and steps are explicit, reference entries remain associated with their definitions, and assemblies identify their member topics.
- **Factual authority:** generated API/CLI facts match pinned sources; authored configuration references have an identified versioned authority.
- **Cross-parser agreement:** IWE and AST compare file manifests and normalized heading/block structure. Neither independently establishes the correctness of the editorial architecture.
- **Publication integrity:** logical relationships resolve, navigation offers appropriate entry points, and old links, images, and anchor targets survive changes.

The earlier reports' 32-file authored-tree scan and 88-file Refdog scan remain useful production-oriented baselines. They should not be read as “32 guide topics versus 88 reference topics.” Together they cover 120 Markdown files, some containing multiple topics or navigation pages.

## Repository-wide production architecture

The repository review covered the content trees, filesystem aliases, both generator directories, publication configuration, navigation generation, analysis/schema tooling, CI, and the vendored Transom entry points. This was an architectural inspection, not a line-by-line audit of vendored dependencies or a regeneration/publication test. All inspected tracked symlinks resolve in this checkout.

### Sources, aliases, and artifacts

| Location | Observed role | Architectural treatment |
| --- | --- | --- |
| `input/` | Canonical website input, mixing authored material, generated Refdog pages, and assets | Publication staging/source tree; generated status must be recorded per object or owned subtree. |
| `doc-input` → `input/` | Alias selected by MkDocs `docs_dir` | Same files, not another source collection. |
| `refdog/input` → `../input/refdog` | Refdog's output path | Writes change canonical publication input immediately; not an isolated generation workspace. |
| `refdog/config/`, `refdog/crds/`, `refdog/cli-doc/` | Editorial inputs and technical-source snapshots | Authoritative generation inputs with version and provenance recorded. CLI Markdown is currently absent from the local snapshot. |
| `refdog/python/` | Active Refdog generation code | Own the model normalization and Markdown generation here, according to the inspected entry point. |
| Root `python/` | Navigation/job-mapping generation, schema runner, and separate copies of reference generators | Distinguish active tools from duplicate modules; establish consumers before consolidating or retiring anything. |
| `config/`, `mkdocs.template.yml`, `mkdocs.yml`, job-mapping CSV | Rendering configuration and publication navigation | Publication concerns, separate from topic identity and authoring ownership. |
| `input/refdog/.pages` | Additional Refdog navigation under the awesome-pages plugin | Part of the publication model even though it is hidden and not a Markdown topic. |
| `input/images/`, `input/refdog/concepts/images/`, `includes/`, CSS/JS files | Content and presentation assets | Inventory their consumers and preserve references; do not classify them as prose topics. |
| `analyse/` | Analyzer implementations, tests, and review documents | Development/review material outside the published content universe. |
| `.iwe/`, `schemas/`, `python/validate_input_docs.py` | Query configuration and proposed document validation | Tool configuration and policy; neither defines the full content architecture by itself. |
| `external/transom/` | Vendored renderer, dependencies, examples, and test sites | Dependency tree; exclude its documentation/examples from the product content inventory. |
| `output/` | Ignored build and analysis artifacts | Reproducible outputs, not authored sources. Use separate directories for each producer. |
| Root reports and historical integration notes | Review artifacts and descriptions of earlier workflows | Record provenance and reconcile obsolete instructions; presence in the repository does not make them website topics. |

The root `python/{commands,resources,concepts,common,generate}.py` files are ordinary files, not symlinks, and each differs from its Refdog counterpart. Their duplication is different from an intentional alias. The [root Plano commands](../.plano.py) do not expose the same generation command as [Refdog's commands](../refdog/.plano.py); do not infer that the root copies are active merely from their names.

### A symlink policy for content and tools

Use canonical, repository-relative content paths such as `input/refdog/resources/site.md` in the shared inventory. Resolve a configured scan root once, then reject duplicate physical targets and avoid recursively following unapproved aliases. Keep the path supplied by the caller as diagnostic information, not as a second document identity. Stable logical topic IDs should survive path changes; absolute real paths should not become publication IDs.

There are two different classes of links here:

- **Content aliases:** `doc-input` and `refdog/input`. They change how the same content is reached, and the latter is a write-through generation destination.
- **Dependency aliases:** root and Refdog `python/{plano,mistune,transom}`, `refdog/external`, and the vendored library/test-site links. They make local imports and development entry points work; they do not add product topics.

For example, `refdog/python/plano` reaches its target through `refdog/external`, which itself points to the root dependency tree. Record/check the chain rather than interpreting the apparent duplicate library paths as separate installations. Preserve symlink behavior when packaging or checking out the repository; checking only that a link entry exists does not establish that its target resolves.

The existing analyzers already avoid recursive symlink traversal during directory discovery, but their root behavior differs from that rule:

| Tool | Current root and scope behavior |
| --- | --- |
| AST CLI | Resolves `--scan` with `realpath`, so an explicitly selected alias can resolve successfully; skips symlink entries below that root. Default scope excludes child directories named `refdog`. |
| IWE wrapper | Resolves the configured library from `.iwe/config.toml` and checks containment in the workspace; discovered keys are relative to that canonical library. Skips child symlink files/directories. Default scope includes Refdog unless excluded. |
| Schema runner | Selects repository `input/` explicitly, excludes every child directory named `refdog`, and skips child symlinks. |

These are directory-discovery behaviors. IWE's explicit `--keys-from` selection takes a different route; it should not be assumed to have passed all the filesystem discovery checks.

Consequently, scanning the repository root and “following everything” is not a valid full-content inventory. It risks duplicate aliases, vendored test content, analyzer fixtures, and generated reports. A full publication audit should select canonical `input/` once and partition it by ownership. With the current AST CLI, that requires two explicit runs—`input/` and `input/refdog/`—because the first excludes the latter. Normalize the Refdog run's path prefix before joining the results to IWE's library-relative paths.

### Observed build paths and discrepancies

The [GitHub Pages workflow](../.github/workflows/main.yaml) installs [the Python requirements](../requirements.txt), runs `mkdocs build`, and deploys `output/docs`. MkDocs reads `doc-input`, which resolves to `input/`. That workflow does **not** regenerate Refdog, regenerate navigation from the CSV, run either analyzer, invoke the schema runner, or build DITA. A successful deployment therefore establishes that the checked-in publication inputs build, not that they match their upstream sources or navigation inputs.

The root `./plano test` instead invokes Transom rendering/link/file checks. Transom uses Mistune for Markdown, while the analysis AST uses remark, and the deployed site uses MkDocs and its configured extensions. Their parsing/rendering contracts are not interchangeable. Compare a deliberately shared Markdown subset, and check extension behavior in the actual publisher.

Refdog's `./plano test` first runs generation, then rendering/link checks. Because `refdog/input` is a symlink, that command can rewrite tracked publication inputs. Do not use it as a supposedly read-only architecture check. The present review did not run it.

Several documentation statements need reconciliation before treating them as an operational contract:

- [The root README](../README.md) and [Refdog README](../refdog/README.md) describe mirroring `refdog/input/` into `input/refdog/`. Here those paths already identify the same directory. Document the alias instead of prescribing a copy between them.
- Refdog's `update_cli` command invokes `../../skupper/generate-doc` from the Refdog working directory, whereas its README describes a different relative location. Specify the required upstream checkout explicitly.
- `update_crds` fetches upstream `main`, while the CLI tool is supplied by a local checkout. A reproducible release build needs a compatible, recorded source set rather than whatever each source happens to contain.
- The CSV/template navigation generator is not a CI step. Define whether generated `mkdocs.yml` is reviewed and committed or produced during the build, and verify agreement accordingly. The trailing `...` and Refdog `.pages` mean CSV navigation alone is not the complete published hierarchy.

The root Transom configuration and MkDocs both use `output/` as an output area, at different levels. Keep analysis under a dedicated review directory and give any future DITA build its own destination and file manifest. Establish the cleanup ownership of each producer before automating builds.

## Roles for AST, IWE, schema checks, and DITA

There should be one reviewed content catalog with several independent checks, rather than a conversion chain in which one parser's output is assumed to prove another's correctness.

| Layer | Useful responsibility | What it cannot establish alone |
| --- | --- | --- |
| Refdog source/model validation | Exact commands/options and resource/field facts, merge precedence, source revisions, declared relationships | Whether a composed page answers a reader's question or renders correctly |
| Remark AST analysis | Original positions, block ownership, section roles, semantic candidates, unsupported source constructs | Whether upstream technical facts or inferred topic types are correct |
| IWE query reports | Independent file/heading/block inventory and an outline suitable for review | Ordered-step semantics, raw-HTML internals, topic type, or DITA validity with the current projection |
| Proposed document schema | Agreed source-shape and metadata constraints | Factual accuracy or publication correctness; a generic schema is not a reviewed model of every topic type |
| MkDocs/Transom publication checks | Navigation, rendered links/assets, extension handling, publication layout | Reproducible upstream extraction or valid DITA |
| Future DITA validation/publication | Chosen grammar, maps, keys, IDs, represented content, and rendered output | Fidelity to sources without comparison to the reviewed catalog |

The existing [schema](../schemas/input-document.yaml) proposes a shared authored-document baseline, including title/introduction expectations and size/depth limits. Its comments call it a proposal; [the runner](../python/validate_input_docs.py) excludes Refdog, requires `schematter`, and is not wired into CI. Keep this status explicit. This review inspected the schema and runner but did not execute schematter or verify the external schema vocabulary. Refdog-generated references and editorial assemblies will need policies appropriate to their roles, not automatic application of an authored-task template.

The current [AST JSON](dita-analyzer.mjs) is an analysis model with mdast blocks, heuristic weights, source ranges, and candidate DITA element names. It is not yet the shared content catalog or a validated DITA intermediate representation. It also does not interpret the proposed ownership/topic metadata. Do not make source edits simply to satisfy a current heuristic when the content's reviewed role says otherwise.

The intended processing paths are:

```text
Authored Markdown -> positioned AST + reviewed topic/section decisions --+
                                                                       |
CLI / CRDs + editorial inputs -> validated Refdog object export ---------+
                                                                       v
                                            common content catalog + relationships
                                                                       |
                              current Markdown publication <-----------+
                                                                       |
                                   future DITA writer -> validation -> publication

IWE inventories and source-schema checks cross-check the selected source artifacts.
They do not replace either the reviewed decisions or upstream fact validation.
```

The two paths need compatible identities, relationships, provenance, and reviewed semantic roles. They do not need to force technical resource properties into generic paragraph-shaped records or force authored explanations into CRD-shaped objects. In the future generated path, IWE/AST checks of generated Markdown remain useful as artifact checks, while DITA can be written from the normalized objects before HTML presentation structure is introduced.

No product DITA topic/map files or DITA writer/build entry point were found in the reviewed repository paths. The analyzer's `dita` naming describes a classification/reporting destination, not an implemented XML conversion capability. Keep that distinction visible in commands, reports, and CI.

## Repository decisions before implementation

| Priority | Decision | Evidence of completion |
| --- | --- | --- |
| First | Canonical content root and alias policy | One manifest representing 120 current Markdown files, each once, plus separately owned asset/navigation manifests; alias targets checked. |
| First | Active generation and publication entry points | Documentation matches the symlinks and commands; each writer's inputs, destinations, and cleanup ownership are declared. |
| First | Source reproducibility and mixed-tree ownership | Pinned CLI/CRD inputs; generated files distinguished from supporting authored topics/assets; no unreviewed rewrite of the shared tree. |
| Next | Topic/assembly contract and reviewed pilot | One concept, task, reference, assembly, and generated object represented without inferring type solely from a folder or heading label. |
| Next | Shared comparison and schema policy | Equivalent canonical scopes in IWE/AST; normalized headings; expected exceptions; role-appropriate structural checks. |
| Next | Navigation and publisher contract | CSV/template/configured navigation reconciled; expected URLs and anchors verified in the deployed renderer. |
| Later | DITA export | Reviewed source/model identities preserved; writer, grammar validation, map/key resolution, and output-fidelity checks implemented. |

These are proposed acceptance criteria, not checks currently enforced by CI. Introduce agreed checks as reviewable changes after the pilot establishes their expected results; do not convert the current heuristic warning count directly into a release gate.

## A small pilot before moving directories

Review four units: the introductory overview, the Refdog Site concept, the Network Observer configuration reference, and its persistent-storage task. Record reader purpose, canonical ownership, semantic type, and desired navigation relationships. Agree which content is intentionally introductory versus detailed, and which task/reference material should be separated.

Then update the model and analyzers to preserve those distinctions. Keep physical paths stable during that work. Only propose directory moves when they improve ownership or authoring workflow enough to justify publication compatibility changes. DITA writing can follow once the same content catalog represents both authored and generated topics clearly.
