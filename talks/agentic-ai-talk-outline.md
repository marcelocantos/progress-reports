# Agentic AI in Anger — Slide Outline

---

## Slide 1: Title

**"One Week, Eleven Repos"**
*What happens when you stop experimenting and start shipping with agentic AI*

Marcelo Cantos
[date]

---

## Slide 2: Let me show you some work

*(No mention of AI yet. Pure engineering showcase.)*

- A spherical chess game on a geodesic board
- A physics-based maze game with 72 levels
- A microthreading library with Go-style channels in C++
- A novel HAMT simplification via multi-round hashing
- A CLI tool overhauled with an interactive installer
- A globe-based game brought to mobile with online multiplayer
- A research paper on universal grammar formalisms

> Speaker note: Show screenshots/demos here. Let the audience assess the work on its own merits. Let them mentally estimate the timeline.

---

## Slide 3: Spherical Chess

*(Visual slide — screenshot or short video of esfera2)*

- Geodesic sphere board — pentagons and hexagons, not squares
- 62 chess pieces with two-pass translucency rendering
- AI opponent with alpha-beta pruning
- 10-lesson interactive tutorial
- iOS standalone app
- Online multiplayer: Go backend, WebSocket relay, matchmaking
- Deployed to OCI with reserved IP and security hardening

---

## Slide 4: Multi-Round Hashing

*(Technical depth slide — diagram of HAMT before/after)*

**Problem**: HAMTs fall back to linear-scan nodes when hash bits run out

**Insight**: Re-hash with an incremented seed to generate unlimited hash bits

**Result**:
- 4 node types → 3
- Dispatch cases: 16 → 9
- Net -280 lines
- Correctness improvement: distinct keys always separate

> Speaker note: This is the slide that earns credibility with the algorithmic thinkers in the room. Walk through the before/after. Emphasise that the net effect was *less* code, not more.

---

## Slide 5: CSP Microthreading

*(Code snippet slide — show the action-RAII pattern)*

```cpp
w << value;  // blocks — the action destructor calls prialt
```

- Cooperative microthreads via Boost.Context
- Typed synchronous channels with independent endpoint lifecycle
- `alt`/`prialt` multiplexing (like Go's `select`)
- Stream combinators: `tee`, `fanout`, `quantize`, `latch`, `killswitch`
- 88 tests passing

---

## Slide 6: The timeline

*(Reveal slide — stark, minimal)*

**One week.**

**~30 human hours.**

153 commits. 11 repos. 5 languages.
C++, Go, Rust, WGSL, Shell.
+23,000 lines. 190 new tests.

> Speaker note: Pause here. Let the dissonance between the work shown and the timeline sink in.

---

## Slide 7: Traditional estimate

| Scenario | Time |
|----------|------|
| Specialist team (4-6 people) | 6-9 months |
| Single talented generalist | 10-18 months |
| What actually happened | ~1 week, ~30 hours |

> Speaker note: These aren't made-up numbers. Walk through why: the diversity tax (12 distinct specialisms), the context-switching penalty, the learning curves. No single person holds geodesic geometry, Go networking, Rust CLI tooling, HAMT theory, PL research, iOS deployment, and C++ ABI expertise simultaneously.

---

## Slide 8: "But is the code any good?"

*(Pre-empt the skepticism)*

- **190 new tests** across 4 repos (including 310 assertions for physics)
- **Security fix**: shell injection eliminated *by construction* — restructured binary/shell boundary
- **Algorithmic elegance**: frozen refactor was net *negative* lines with fewer node types
- **Production deployed**: esfera2 running on OCI with multiplayer

This is not "vibe coding."

---

## Slide 9: What did the human actually do?

| Human | AI |
|-------|-----|
| "I want chess on a sphere" | Geodesic geometry, vertex welding, winding order |
| "Use multi-round hashing" | Worked through every HAMT operation, handled edge cases |
| "The physics feel is off" | Tuned friction, repulsion, spring constants |
| "Extract csp from bricabrac" | Renamed namespace, restructured headers, verified 88 tests |
| "Survey grammar formalisms" | Read and synthesised 8 related systems into a 717-line paper |

**Vision. Taste. Architectural judgement. Domain insight.**
The AI provides breadth, speed, and tirelessness.

---

## Slide 10: The 12 specialisms

*(Visual: a grid or wheel showing the domains)*

- WebGPU/Dawn rendering + WGSL shaders
- Geodesic geometry + spherical topology
- Custom rigid-body physics
- Go networking (TCP, WebSocket, REST)
- Rust CLI tooling
- iOS + Android native
- ASTC/ETC2 texture compression + mip streaming
- OCI cloud deployment + security
- HAMT algorithm design + hash theory
- C++ microthreading + ABI
- Programming language theory + grammar formalisms
- IEEE 754 decimal arithmetic

**One person. One week. Zero context-switch penalty.**

> Speaker note: This is the real superpower. Not "AI writes code faster" but "AI eliminates the cost of moving between domains." A human trying to hold all twelve of these at once would burn most of their energy on ramp-up and context recovery.

---

## Slide 11: It's not about speed

*(Reframing slide)*

The multiplier isn't "do the same work faster."

It's: **projects that were never economically viable become viable.**

- The wbnf research paper would never have been written
- Spherical chess would have stayed an idea
- The csp library would have stayed buried in a monorepo
- The frozen simplification would have waited for a quiet month that never comes

---

## Slide 12: What this means for us

*(Call to action — adapt to your workplace)*

- This is not a future capability. It works today.
- The gap between teams using this and teams not using this will compound.
- The biggest risk isn't adopting too fast. It's adopting too slow while others don't.

**What would YOUR impossible project list look like with a 20-50x multiplier?**

---

## Slide 13: How to start

*(Practical guidance)*

1. **Pick a real project, not a toy.** The gains show up at scale, not on fizzbuzz.
2. **Think in terms of direction, not dictation.** Describe what you want, iterate on the result.
3. **Trust but verify.** Write tests. Review diffs. The AI is a tireless collaborator, not an oracle.
4. **Lean into breadth.** The biggest wins come from work that crosses domain boundaries — the stuff you'd never attempt alone.

---

## Slide 14: Close

**"The cost of not adopting this is not 'we're slower.'**
**It's 'we never attempt the things that would have mattered.'"**

[Link to weekly report gist]
