# Architecture Language

Shared vocabulary for architecture-deepening reviews. Use these terms exactly. Avoid substituting generic words that blur the recommendation.

## Terms

**Module**
Anything with an interface and an implementation. This is deliberately scale-agnostic: a module can be a function, class, package, process, or vertical slice.

Avoid: unit, component, service.

**Interface**
Everything a caller must know to use the module correctly. This includes type signatures, invariants, ordering constraints, error modes, required configuration, and performance characteristics.

Avoid: API, signature. Those usually describe only part of the interface.

**Implementation**
The code and behavior hidden inside a module. Use implementation when discussing what lives behind the interface.

**Depth**
Leverage at the interface. A module is deep when callers get substantial behavior through a small interface. A module is shallow when using it is almost as complex as knowing its implementation.

**Seam**
The place where a module's interface lives and behavior can vary without editing callers. Choosing the seam is a design decision.

Avoid: boundary. It is overloaded with domain-driven design language.

**Adapter**
A concrete implementation that satisfies an interface at a seam. Adapter describes the role at the seam, not the size or complexity of the code.

**Leverage**
What callers get from depth: one interface provides useful capability across many call sites and tests.

**Locality**
What maintainers get from depth: changes, bugs, verification, and domain knowledge concentrate in one place instead of spreading across callers.

## Principles

- Depth is a property of the interface, not the implementation.
- A deep module can still have internal seams used by its own implementation and tests.
- The deletion test: if deleting a module removes complexity, it was pass-through; if complexity reappears across callers, it was earning its keep.
- The interface is the test surface. Callers and tests should cross the same seam.
- One adapter means a hypothetical seam. Two adapters means a real seam.

## Relationships

- A Module has an Interface and an Implementation.
- Depth is measured at the Interface.
- A Seam is where a Module's Interface lives.
- An Adapter sits at a Seam.
- Depth creates Leverage for callers and Locality for maintainers.

## Rejected framings

- Do not measure depth as implementation line count divided by interface line count; that rewards padded implementations.
- Do not treat Interface as only a TypeScript `interface`, public method set, or type signature.
- Do not call every extracted abstraction a Seam; it is a seam only if behavior can actually vary there.
