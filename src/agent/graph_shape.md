```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	google_search(google_search)
	summarize(summarize)
	__end__([<p>__end__</p>]):::last
	__start__ --> google_search;
	google_search --> summarize;
	summarize --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc

```