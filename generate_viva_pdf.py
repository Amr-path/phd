#!/usr/bin/env python3
"""Generate Viva Prep Q&A PDF using reportlab."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

doc = SimpleDocTemplate("/home/user/phd/Viva_Preparation_QA_Guide.pdf", pagesize=A4,
                        topMargin=2*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='SectionTitle', fontSize=15, leading=20, textColor=HexColor('#003366'),
                          spaceAfter=10, spaceBefore=20, backColor=HexColor('#E6F0FA'), borderPadding=6, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='Question', fontSize=11, leading=15, textColor=HexColor('#990000'),
                          spaceAfter=4, spaceBefore=12, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='Answer', fontSize=10, leading=14, textColor=HexColor('#000000'),
                          spaceAfter=8, spaceBefore=2, fontName='Helvetica', leftIndent=10))
styles.add(ParagraphStyle(name='TitleMain', fontSize=22, leading=28, textColor=HexColor('#003366'),
                          alignment=TA_CENTER, spaceAfter=10, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='SubTitle', fontSize=13, leading=18, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle(name='CenterNormal', fontSize=11, leading=15, alignment=TA_CENTER, spaceAfter=4))

story = []

# Title page
story.append(Spacer(1, 4*cm))
story.append(Paragraph('PhD Viva Voce Preparation Guide', styles['TitleMain']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph('Dynamic Pathfinding for Autonomous Systems:<br/>An Efficient Grid-Map Framework for Classical Search', styles['SubTitle']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph('<b>Elshahed Amr Moustafa Mohamed Aly Elsayed</b>', styles['CenterNormal']))
story.append(Paragraph('Doctor of Philosophy | Universiti Sains Malaysia | 2026', styles['CenterNormal']))
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph('<i>Comprehensive Q&amp;A guide with 60 possible viva questions and detailed answers</i>', styles['CenterNormal']))
story.append(PageBreak())

def section(title):
    story.append(Paragraph(title, styles['SectionTitle']))

def qa(num, q, a):
    story.append(Paragraph(f'Q{num}: {q}', styles['Question']))
    story.append(Paragraph(a.replace('\n','<br/>'), styles['Answer']))

# ===================== SECTION 1 =====================
section('SECTION 1: OPENING &amp; GENERAL QUESTIONS')

qa(1, 'Can you summarize your thesis in 3-5 minutes?',
   'My thesis addresses the problem of making pathfinding faster for autonomous systems in biosecurity-sensitive environments such as agricultural facilities, healthcare settings, and ports.\n\n'
   'The core idea is simple: instead of letting a search algorithm explore the entire grid map, I confine it to a narrow "corridor" drawn along the straight line between start and goal. This is the <b>Incremental Line Search (ILS)</b> framework.\n\n'
   'The flow is:\n'
   '1. Draw a Bresenham line from start to goal.\n'
   '2. Build a corridor of fixed width around that line.\n'
   '3. Run any classical search algorithm (A*, Dijkstra, BFS, DFS, or Best-First) inside that corridor only.\n'
   '4. If no path is found, widen the corridor and retry.\n\n'
   'Results on 6,000 synthetic 200x200 grids showed an average <b>87.31% reduction in execution time</b> and <b>71.44% reduction in node expansions</b>. Path optimality was preserved for optimal algorithms.\n\n'
   'My second contribution, <b>Adaptive ILS (AILS)</b>, uses integral images to estimate local obstacle density and adjusts the corridor width at each point -- narrow in open areas, wider near obstacles. AILS achieved 51-56% node reduction on 200x200 grids, scaling to <b>76.8% on 500x500 grids</b>. The Predictive strategy achieved <b>99.8% optimality</b>.\n\n'
   'The two methods are complementary: ILS excels on uniform-density environments, while AILS provides robustness across heterogeneous obstacle layouts.')

qa(2, 'What motivated you to choose this research topic?',
   'Three things came together:\n\n'
   '<b>1. Real-world need:</b> Autonomous systems in biosecurity settings -- drones surveying contamination zones, robots in quarantine areas, vehicles in ports -- need to compute paths quickly and safely. Standard algorithms like A* can be too slow on large or cluttered grids.\n\n'
   '<b>2. A gap in the literature:</b> Jump Point Search achieves dramatic speedups but only works on uniform-cost grids. For risk-annotated grids (where each cell has a different cost reflecting danger level), there was no equivalent corridor-based approach.\n\n'
   '<b>3. Practical observation:</b> In most navigation scenarios, the optimal path does not deviate far from the straight line between start and goal. This geometric insight suggested that confining search to a narrow band could work well in practice.')

qa(3, 'What is your original contribution to knowledge?',
   '<b>Contribution 1 -- Incremental Line Search (ILS):</b> A general framework that wraps any classical search algorithm inside a corridor constraint. Unlike JPS, ILS works with any edge-cost model. It achieved 87.31% execution-time reduction and 71.44% node reduction on average. For non-optimal algorithms like DFS, ILS also dramatically improved path quality (up to 93.74% path-length reduction).\n\n'
   '<b>Contribution 2 -- Adaptive ILS (AILS):</b> Uses integral images for O(1) local density estimation and constructs a variable-width corridor. Three strategies (Base, Standard, Predictive) are selected automatically. The Predictive strategy achieved 62.2% time improvement with 99.8% optimality.')

qa(4, 'Why is this research significant?',
   '<b>1. Computational efficiency:</b> ILS and AILS enable real-time pathfinding on large grids using commodity hardware, without GPU acceleration.\n\n'
   '<b>2. Generality:</b> Unlike JPS (uniform costs only) or hierarchical methods (require preprocessing), ILS/AILS work with any search algorithm and any cost model, with no static preprocessing.\n\n'
   '<b>3. Broader applicability:</b> While biosecurity is the motivating context, the techniques apply to warehouse automation, agricultural robots, search-and-rescue, and any grid-based planning scenario.')

# ===================== SECTION 2 =====================
story.append(PageBreak())
section('SECTION 2: RESEARCH DESIGN &amp; METHODOLOGY')

qa(5, 'Why did you use synthetic grids instead of real-world benchmarks like Moving AI?',
   'Synthetic grids were a deliberate methodological choice:\n\n'
   '<b>1. Precise control:</b> Synthetic grids let me control exactly two variables -- obstacle density and topology -- while holding everything else constant.\n\n'
   '<b>2. Statistical power:</b> I generated 6,000 maps for ILS (2,000 per density) and hundreds of configurations for AILS.\n\n'
   '<b>3. Five controlled topologies:</b> Random, Clustered, Maze, Room, and Open patterns cover a wide range of structural characteristics.\n\n'
   '<b>4. Real-world validation:</b> I did test on a satellite-derived grid (DS4) to show ILS generalizes beyond synthetic conditions.\n\n'
   '<b>5.</b> Moving AI benchmarks are identified as the immediate next step for external validation.')

qa(6, 'Why did you choose the Bresenham line as the corridor axis?',
   '<b>1.</b> It is the best discrete approximation of the straight line using only integer arithmetic.\n\n'
   '<b>2.</b> It runs in O(L) time -- essentially free compared to the search itself.\n\n'
   '<b>3.</b> In most practical navigation scenarios (open fields, warehouses, agricultural rows), the optimal path stays close to the straight line.\n\n'
   'The limitation is that when the optimal path deviates significantly (maze/room patterns), the Bresenham reference becomes a poor approximation. This is acknowledged as a limitation.')

qa(7, 'How do you justify using five different algorithms?',
   '<b>1. Generality claim:</b> By showing ILS works across optimal (A*, Dijkstra, BFS) and non-optimal (DFS, Best-First) algorithms, I demonstrate corridor restriction is a general-purpose wrapper.\n\n'
   '<b>2. Different insights:</b> Optimal algorithms showed ILS preserves optimality. Non-optimal algorithms revealed an unexpected bonus -- DFS path length dropped by up to 93.74%.\n\n'
   '<b>3. Practical relevance:</b> In resource-constrained embedded systems, simpler algorithms like BFS or DFS may be preferred due to lower memory requirements.')

qa(8, 'Explain the preprocessing pipeline.',
   'Nine standardized steps:\n'
   'Step 1: Image acquisition (or procedural generation)\n'
   'Step 2: Greyscale conversion\n'
   'Step 3: Binary thresholding (threshold = 128)\n'
   'Step 4: Grid construction (pixels to vertices, edges based on connectivity)\n'
   'Step 5: Obstacle density verification (within 1% of target)\n'
   'Step 6: Start and goal assignment\n'
   'Step 7: Reachability check (BFS)\n'
   'Step 8: Integral image computation (AILS only, O(|V|))\n'
   'Step 9: Output preprocessed grid\n\n'
   'Each step has a clear purpose. The pipeline ensures all grids undergo identical processing.')

qa(9, 'How does the integral image enable O(1) density queries?',
   'An integral image (summed-area table) stores cumulative sums. For each cell (x,y), I(x,y) = sum of all obstacle values in the rectangle from (0,0) to (x,y).\n\n'
   'To find the obstacle count in any rectangular window:\n'
   'count = I(x2,y2) - I(x1-1,y2) - I(x2,y1-1) + I(x1-1,y1-1)\n\n'
   'This takes exactly 4 lookups and 3 arithmetic operations -- O(1) regardless of window size. Building the integral image takes O(|V|) time (one pass). After that, every density query is O(1).')

qa(10, 'Why three corridor strategies? Why not always use Predictive?',
   '<b>Base (fixed-width):</b> Used when Bresenham line is obstacle-free. No density computation needed -- cheapest.\n\n'
   '<b>Standard (density-adaptive):</b> Used when obstacles exist but density changes gradually.\n\n'
   '<b>Predictive (gradient-enhanced):</b> Used when density changes rapidly. Widens corridor BEFORE dense regions.\n\n'
   'Why not always Predictive? It adds gradient computation overhead. On obstacle-free lines, Base is sufficient and faster. The automatic selection ensures each query gets the cheapest sufficient strategy.')

qa(11, 'What is the time complexity of ILS and AILS?',
   '<b>ILS:</b> Bresenham: O(L). Corridor: O(L*w). Search: O(|C|*log|C|) for A*. Worst case (full expansion): same as unconstrained O(N log N). Best case: O(L*w*log(L*w)) -- much smaller.\n\n'
   '<b>AILS:</b> Integral image: O(|V|). Density queries: O(1) each, O(L) total. Corridor: O(sum of r(p)^2). Search: O(|C_a|*log|C_a|). Fallback: O(boundary*delta_r) per expansion.\n\n'
   'Key insight: |C| &lt;&lt; |V| in practice, so effective complexity is much lower than full-grid search.')

qa(12, 'Why paired t-tests and Cohen\'s d? Are these appropriate?',
   '<b>Paired t-tests:</b> Each map was run with both standard and corridor-based algorithms. Pairing removes between-map variance. Normality verified with Shapiro-Wilk (W > 0.97, p > 0.10).\n\n'
   '<b>Cohen\'s d:</b> With 2,000 maps per density, almost any tiny difference becomes statistically significant. Cohen\'s d tells whether the difference MATTERS:\n'
   '- AILS-Base vs A*: d = 0.82 (large effect)\n'
   '- AILS-Adaptive vs A*: d = 0.76 (medium-to-large effect)\n\n'
   'For multi-group comparisons, one-way ANOVA with Tukey HSD correction was used.')

# ===================== SECTION 3 =====================
story.append(PageBreak())
section('SECTION 3: ILS-SPECIFIC QUESTIONS')

qa(13, 'How does ILS preserve path optimality?',
   'Within the corridor, A*, Dijkstra, and BFS retain all original guarantees. The only modification is filtering out cells outside the corridor. Within the corridor, algorithms work exactly as normal.\n\n'
   'The path returned is <b>optimal within the corridor</b>. If the corridor contains the globally optimal path (which it does in most cases at 10-25% density), the result is also globally optimal.\n\n'
   'BFS and Dijkstra returned identical discrete path costs. A* with line-of-sight post-processing produced shorter Euclidean paths (69.54-86.37% improvement) while discrete optimality was preserved.\n\n'
   'The incremental expansion provides a safety net: if the initial corridor misses the optimal path, widening will eventually include it.')

qa(14, 'Why does ILS improve DFS path quality so dramatically (up to 93.74%)?',
   'Unconstrained DFS explores depth-first -- it can chase a single branch all the way to a distant corner before backtracking. The resulting path can be absurdly long.\n\n'
   'The corridor completely changes DFS behavior. Instead of 40,000 cells to wander through (200x200 grid), DFS is funneled into 2,000-5,000 corridor cells. The worst-case path within that corridor is inherently much shorter.\n\n'
   'This was an unexpected but valuable finding -- ILS acts as an <b>implicit quality guide</b> for non-optimal algorithms.')

qa(15, 'What happens when the initial corridor doesn\'t contain a valid path?',
   '<b>ILS fallback:</b> Width incremented by delta_w, corridor rebuilt, search restarted. Continues until path found or corridor = full grid.\n\n'
   '<b>AILS fallback:</b> More efficient local expansion. BFS from corridor boundary adds cells within Chebyshev distance delta_r. Only boundary expanded, not entire corridor.\n\n'
   'This ensures <b>completeness</b>: if a path exists, it will be found. The cost of fallback is the main reason performance degrades on high-density environments.')

qa(16, 'How did you choose the initial corridor width?',
   '<b>ILS:</b> w_0 = floor(gamma * min(H,W)). Proportional sizing ensures corridor scales with grid size.\n\n'
   '<b>AILS:</b> r_min=2 (default), r_max=ceil(0.1*min(H,W)). The ablation study confirmed:\n'
   '- (r_min=2, r_max=ceil(0.1*min(H,W))) achieved 99.8% optimality with minimal overhead\n'
   '- Smaller radii: faster but lower optimality (94.3%)\n'
   '- Larger radii: perfect optimality but slower')

qa(17, 'The ILS results exceeded your hypothesized 40-70% reduction. Why?',
   'The hypothesis (RH1) predicted 40-70% reductions. Actual: 87.31% (time) and 71.44% (nodes).\n\n'
   'Conservative prediction was based on literature for corridor methods. Actual results exceeded because:\n'
   '1. The corridor was effective at ALL tested densities (10-30%)\n'
   '2. Best-First responded especially well (95.52% at 10%)\n'
   '3. Bresenham line was a better approximation than anticipated\n\n'
   'Having predictions exceeded is positive -- the hypothesis served its purpose of providing a testable prediction.')

# ===================== SECTION 4 =====================
story.append(PageBreak())
section('SECTION 4: AILS-SPECIFIC QUESTIONS')

qa(18, 'Explain the density-adaptive radius formula.',
   'r(p) = r_min + floor((r_max - r_min) * sigma(p)^alpha)\n\n'
   '- sigma(p): local obstacle density at point p (via integral image, O(1))\n'
   '- r_min (default 2): minimum radius for obstacle-free regions\n'
   '- r_max (default ceil(0.1*min(H,W))): maximum radius for fully blocked regions\n'
   '- alpha (default 1.0): controls how aggressively radius responds to density\n\n'
   'When sigma=0: r(p)=r_min (narrow). When sigma=1: r(p)=r_max (widest). alpha&lt;1: wide early. alpha&gt;1: narrow longer. Ablation showed alpha=1.0 optimal: 98.7% optimality.')

qa(19, 'Why does AILS have higher execution time than A* on grids smaller than 300x300?',
   'AILS has fixed overhead: integral image O(|V|), per-point density queries, hash-set assembly, corridor membership checks.\n\n'
   'On small grids, search is already fast (A* takes 0.95ms on 50x50). AILS overhead (3.94ms) exceeds total search time. Node savings (5.1%) too small to compensate.\n\n'
   'At 300x300, crossover: AILS 6.3% faster (29.61ms vs 31.62ms) with 65.5% fewer nodes. On 500x500: 76.8% fewer nodes. In C++, crossover would occur at smaller grids.')

qa(20, 'Why does AILS fail on Maze, Room, and Clustered patterns?',
   'Root cause: optimal path deviates significantly from the Bresenham reference line.\n\n'
   '<b>Maze</b> (50.5% density): path must follow winding passages. Bresenham cuts through walls.\n'
   '<b>Room</b> (90.9% density): path threads through narrow doorways that don\'t align with line. AILS 116x slower.\n'
   '<b>Clustered</b> (27% density): large clusters force path around them. 70x slower.\n\n'
   'Fundamental issue: AILS\'s corridor is anchored to a straight-line approximation. When the environment requires winding/detouring, this breaks down. Explicitly acknowledged as a limitation.')

qa(21, 'Explain the Predictive strategy and why it achieves 99.8% optimality.',
   'Predictive adds density gradient: r(p) = r_min + floor((r_max - r_min) * (sigma(p) + beta*|grad sigma(p)|)^alpha)\n\n'
   'When gradient is large, obstacle concentration is CHANGING rapidly. Predictive widens the corridor BEFORE reaching the dense region.\n\n'
   'Most suboptimality comes from the corridor being too narrow when hitting a dense region. Predictive avoids this by preemptively widening, so the optimal path is already inside the corridor. The 0.2% non-optimal cases are instances where gradient was not a reliable predictor.')

qa(22, 'How does automatic strategy selection work?',
   'Single scan of Bresenham line at initialization:\n'
   '1. Compute sigma(p) and gradient for all p on the line\n'
   '2. If sigma(p)=0 for ALL points --> Base (cheapest)\n'
   '3. Else if max|gradient| &lt; 0.1 --> Standard\n'
   '4. Else --> Predictive\n\n'
   'Zero-cost in practice: density computations are already needed for corridor construction. Selection logic adds only a max-reduction over gradient values.')

# ===================== SECTION 5 =====================
story.append(PageBreak())
section('SECTION 5: RESULTS &amp; STATISTICAL ANALYSIS')

qa(23, 'Walk us through the key numerical results.',
   '<b>ILS Results (DS1, 6000 maps, 200x200):</b>\n'
   '- Average time reduction: 87.31% | Node reduction: 71.44%\n'
   '- Best single: Best-First at 10% density -- 95.52% time reduction\n'
   '- DFS path improvement: up to 93.74% | All p &lt; 0.05\n\n'
   '<b>AILS Results (DS2/DS3):</b>\n'
   '- Node reduction 200x200: 51-56% (d=0.76-0.82, p&lt;0.001)\n'
   '- Node reduction 500x500: 76.8% | Crossover: ~300x300\n'
   '- Predictive: 62.2% time improvement, 99.8% optimality\n\n'
   '<b>Ablation:</b> Optimal defaults: r_min=2, r_max=ceil(0.1*min(H,W)), alpha=1.0, omega=3')

qa(24, 'Why do improvements decrease as obstacle density increases?',
   'At higher densities:\n'
   '1. More corridor expansions triggered -- dense obstacles block paths within initial corridor\n'
   '2. Corridor fraction of grid increases\n'
   '3. Paths deviate more from straight line\n\n'
   'A* time improvement: 94.81% at 10% --> 82.77% at 30%. Even at 30%, improvements stayed above 80% for A*, DFS, and Best-First. Best at 10-25% density -- common in outdoor robotics and warehouses.')

qa(25, 'The ILS and AILS experiments used different hardware. How can you compare them?',
   'ILS: Apple M1 MacBook Air (8GB). AILS: Intel i7-12700K (64GB DDR5). Absolute times NOT directly comparable.\n\n'
   'All cross-study comparisons use RELATIVE, hardware-independent metrics:\n'
   '- Percentage improvement (relative to baseline on SAME hardware)\n'
   '- Node reduction (completely hardware-independent)\n'
   '- Corridor efficiency, optimality rate\n\n'
   'This is explicitly acknowledged as a limitation. Node count comparisons are always valid.')

qa(26, 'Why didn\'t you test on grids larger than 500x500?',
   '1. Trend was clear: 5.1% (50x50) to 76.8% (500x500) -- consistent upward trend\n'
   '2. Crossover already captured at 300x300\n'
   '3. Python overhead on very large grids would obscure algorithmic benefits\n'
   '4. 200x200 to 500x500 covers many real-world scenarios\n\n'
   'C++ reimplementation for larger-scale testing identified as future work.')

qa(27, 'No formal sub-optimality bound -- isn\'t that a significant weakness?',
   'Recognized limitation, not fatal:\n\n'
   '<b>Why no bound:</b> Optimality gap is instance-dependent. AILS corridor is non-convex. Worst-case gives vacuous bound.\n\n'
   '<b>Why not fatal:</b>\n'
   '1. Empirically 99.8% optimal (Predictive), paths within 1-3% when not exact\n'
   '2. Fallback ensures full-grid search if needed\n'
   '3. Weighted A* also lacks tight practical bounds\n'
   '4. Future work: instance-specific or probabilistic bounds')

# ===================== SECTION 6 =====================
story.append(PageBreak())
section('SECTION 6: LITERATURE &amp; THEORETICAL QUESTIONS')

qa(28, 'How does ILS compare to Jump Point Search (JPS)?',
   '<b>JPS:</b> Exploits path symmetry. Prunes intermediate nodes. 10-100x speedup. RESTRICTED to uniform-cost grids. Modifies A* internal logic.\n\n'
   '<b>ILS:</b> Exploits geometric proximity to straight line. Restricts entire search to corridor. Any cost model. Any algorithm as wrapper.\n\n'
   'The two are compatible: JPS could serve as base algorithm inside ILS corridor on uniform grids. ILS fills the gap JPS leaves: risk-annotated grids where costs vary.')

qa(29, 'How does your work relate to D* Lite and LPA*?',
   'D* Lite/LPA* are <b>incremental replanning</b> methods -- maintain search trees across episodes, repair solutions when environment changes. But full-grid memory, no scope constraint.\n\n'
   'ILS/AILS are <b>search-space restriction</b> methods -- constrain WHERE to look within a single query.\n\n'
   '<b>Complementary:</b> D* Lite inside AILS corridor = memory savings + incremental repair. ILS restricts spatial scope; D* Lite restricts temporal scope.')

qa(30, 'Why didn\'t you use learning-based approaches?',
   '1. <b>Formal guarantees:</b> Classical search provides provable optimality. Neural heuristics may violate admissibility.\n'
   '2. <b>Generalization:</b> Learned models may fail in novel settings. ILS/AILS work on any grid without training.\n'
   '3. <b>Interpretability:</b> Classical algorithms are fully traceable -- important for safety certification.\n'
   '4. <b>No training data needed:</b> Works out of the box.\n\n'
   'A hybrid approach (learned corridor axis, classical search within) is an interesting future direction.')

qa(31, 'What is the relationship between your work and Theta*?',
   'ILS borrows line-of-sight POST-PROCESSING from Theta*. After finding a path, if a vertex\'s grandparent has clear line of sight, the intermediate parent is removed.\n\n'
   'Key difference: Theta* modifies A*\'s internal expansion logic. ILS applies post-processing AFTER the standard search -- so it works with ANY algorithm (including DFS and BFS).\n\n'
   'Observed improvements (69.54-86.37%) consistent with Theta* literature.')

qa(32, 'How does your work address the two research gaps?',
   '<b>Gap 1:</b> No corridor-constrained search for risk-annotated grids. JPS needs uniform costs, subgoal methods need static preprocessing.\n'
   '--> <b>ILS</b> fills this: any cost model, no preprocessing.\n\n'
   '<b>Gap 2:</b> No adaptive search-scope mechanism for dynamic replanning. D* Lite maintains full-grid structures.\n'
   '--> <b>AILS</b> fills this: dynamically adjusts corridor width based on local density.\n\n'
   'Gap 1 --> O1 --> ILS. Gap 2 --> O2 --> AILS.')

# ===================== SECTION 7 =====================
story.append(PageBreak())
section('SECTION 7: BIOSECURITY APPLICATION QUESTIONS')

qa(33, 'How exactly does pathfinding relate to biosecurity?',
   '1. <b>Physical navigation:</b> Drones/robots navigate agricultural facilities, quarantine areas, ports, healthcare settings where biosecurity risks exist.\n\n'
   '2. <b>Risk-aware pathfinding:</b> Paths must minimize exposure to biological hazards. ILS/AILS support weighted cost models: cost(n,n\') = dist(n,n\') + lambda * r(n\').\n\n'
   '3. <b>Real-time response:</b> When contamination detected, autonomous systems need to replan quickly. 87% time reduction enables faster response.\n\n'
   '4. <b>Port security:</b> Ports are critical biosecurity nodes -- entry points for biological threats.')

qa(34, 'Your experiments don\'t include actual biosecurity scenarios. How do you justify the framing?',
   '1. The thesis develops GENERAL-PURPOSE techniques. Biosecurity provides MOTIVATION and CONTEXT.\n'
   '2. Any biosecurity environment can be represented as an occupancy grid with risk annotations -- my algorithms work on this abstraction.\n'
   '3. DS4 demonstrates real-world applicability on satellite-derived grid.\n'
   '4. Density ranges tested (10-25%) match real biosecurity environments.\n'
   '5. Biosecurity is the motivating USE CASE, not the experimental testbed. Full biosecurity evaluation is future work.')

qa(35, 'How would ILS/AILS handle dynamic risk maps?',
   '1. <b>ILS:</b> Re-run from scratch with updated grid. Fast enough (87% reduction) for moderate update frequencies.\n'
   '2. <b>AILS:</b> Re-compute integral image O(|V|), rebuild corridor. Naturally responds to new distribution.\n'
   '3. <b>Combined with D* Lite:</b> Repair only affected plan portions within corridor.\n'
   '4. Designed for "moderate, piecewise-static dynamics" -- realistic for biosecurity where updates come from lab tests (hours) or sensor readings (minutes).')

# ===================== SECTION 8 =====================
story.append(PageBreak())
section('SECTION 8: LIMITATIONS &amp; FUTURE WORK')

qa(36, 'What are the main limitations of your work?',
   '1. <b>Overhead on small grids:</b> AILS slower than A* below ~300x300.\n'
   '2. <b>High-density &amp; structured environments:</b> Degrades above 30% density; poor on maze/room/clustered.\n'
   '3. <b>No formal sub-optimality bound:</b> 99.8% empirical but no worst-case guarantee.\n'
   '4. <b>Synthetic benchmarks:</b> External validation on Moving AI needed.\n'
   '5. <b>Different hardware:</b> Cross-study uses relative metrics only.\n'
   '6. <b>Parameter dependence:</b> No automatic tuning mechanism.')

qa(37, 'If you had another year, what would you do?',
   '1. Moving AI benchmark evaluation\n'
   '2. C++ implementation (push crossover to smaller grids)\n'
   '3. Formal sub-optimality analysis\n'
   '4. Combine with D* Lite for dynamic replanning\n'
   '5. Multi-agent pathfinding extension\n'
   '6. Learned corridor axis prediction\n'
   '7. Hardware deployment on actual robots/drones\n'
   '8. Automatic parameter tuning')

qa(38, 'Would results be different in C++?',
   '<b>Algorithmic results</b> (node counts, corridor sizes, optimality rates): <b>identical</b> -- language-independent.\n\n'
   '<b>Timing results:</b> Much faster absolute times. Time-efficiency crossover would shift to smaller grids. Performance gap at small sizes would narrow.\n\n'
   'This is why I report both timing metrics (implementation-dependent) and node counts (implementation-independent) -- node counts are the true measure of algorithmic efficiency.')

qa(39, 'How would you extend to 3D?',
   '1. <b>3D Bresenham:</b> Generalizes naturally to 3D.\n'
   '2. <b>3D corridor:</b> Becomes a tube. Density window becomes a cube. Integral image becomes 3D summed-volume table.\n'
   '3. <b>Savings scale better:</b> Corridor volume = O(L*r^2) vs grid = O(N^3). Even larger fraction savings.\n'
   '4. Relevant for UAV navigation, underwater vehicles, surgical robotics.')

# ===================== SECTION 9 =====================
story.append(PageBreak())
section('SECTION 9: CHALLENGING QUESTIONS')

qa(40, 'Isn\'t a corridor-based approach just a heuristic hack?',
   'I would push back on "hack":\n'
   '1. <b>Formal definition:</b> Corridor rigorously defined (Definition 3.1). Adaptive radius has clear mathematical structure.\n'
   '2. <b>Completeness:</b> Fallback expansion guarantees path is found if one exists.\n'
   '3. <b>Within-corridor optimality:</b> Provably optimal within the corridor for optimal algorithms.\n'
   '4. <b>Geometric justification:</b> Bresenham line is the optimal discrete straight-line approximation.\n'
   '5. <b>Systematic evaluation:</b> 5 algorithms, 3 densities, 8 grid sizes, 5 topologies, rigorous statistics.')

qa(41, 'Your method fails on maze/room patterns. Doesn\'t that severely limit applicability?',
   '<b>1. Target domain:</b> Outdoor robotics, warehouses, agricultural fields, ports. These are open/random patterns at 10-25% density -- exactly where ILS/AILS excels. Mazes (50-90% density) are not typical.\n\n'
   '<b>2. Algorithm selection:</b> A well-designed system characterizes the environment and selects appropriately. For mazes, use A*. For open environments, use ILS/AILS.\n\n'
   'No single algorithm dominates all scenarios. The value is providing a superior tool for a practically important class of environments.')

qa(42, 'Why should we care about DFS with ILS?',
   '1. <b>Generality demonstration:</b> Proves corridor is a general-purpose wrapper.\n'
   '2. <b>Theoretical insight:</b> Revealed the corridor acts as an implicit quality guide -- would not emerge from testing only optimal algorithms.\n'
   '3. <b>Resource-constrained systems:</b> DFS uses O(d) memory vs O(b^d) for BFS/A*. With ILS, DFS becomes viable on constrained platforms.\n'
   '4. <b>Completeness:</b> Including all algorithms prevents cherry-picking.')

qa(43, 'The 87.31% time reduction seems too good. Could there be a bug?',
   'Safeguards:\n'
   '1. <b>Paired comparison:</b> Same map, same machine, same session.\n'
   '2. <b>Consistent metrics:</b> Time (87.31%) aligned with nodes (71.44%).\n'
   '3. <b>Statistical validation:</b> p &lt; 0.05 across 2,000 maps per density.\n'
   '4. <b>Expected trend:</b> Improvements decrease with density -- not arbitrary.\n'
   '5. <b>Median of three runs.</b>\n'
   '6. <b>Geometric reasoning:</b> At 10% density, corridor covers &lt;10% of grid. Searching 10% of space naturally yields ~90% savings.')

qa(44, 'Why not compare against Contraction Hierarchies or HPA*?',
   '1. <b>Correct baseline:</b> ILS/AILS modify how classical algorithms explore. Right comparison is "same algorithm with vs without corridor."\n'
   '2. <b>Different categories:</b> CH/HPA* need expensive offline preprocessing. ILS/AILS are online with no preprocessing.\n'
   '3. <b>Different use cases:</b> Static map + many queries --> preprocessing wins. Dynamic map + single queries --> ILS/AILS more suitable.\n'
   '4. A fair comparison requires same language, same hardware -- identified as future work.')

# ===================== SECTION 10 =====================
story.append(PageBreak())
section('SECTION 10: PUBLICATION &amp; CONTRIBUTION QUESTIONS')

qa(45, 'What papers have you published from this thesis?',
   'Two papers:\n'
   '1. Elshahed (2025) - ILS paper: Incremental Line Search framework on DS1/DS4. Covers Objective O1.\n'
   '2. Elshahed (2025) - AILS paper: Adaptive ILS framework on DS2/DS3. Covers Objective O2.\n'
   'Referenced as [Elshahed2025ILS] and [Elshahed2025AILS] throughout.')

qa(46, 'How does your work advance the field beyond incremental improvements?',
   '1. <b>New paradigm:</b> Corridor-constrained search for non-uniform-cost grids did not exist. Occupies a new point in the design space.\n'
   '2. <b>Algorithm-agnostic wrapper:</b> Novel idea that corridor restriction can wrap ANY search algorithm.\n'
   '3. <b>Unexpected finding:</b> Path-quality improvement for non-optimal algorithms (DFS 93.74%) not anticipated by prior work.\n'
   '4. <b>Practical impact:</b> Real-time pathfinding on commodity hardware for grid sizes that previously required more power.')

# ===================== SECTION 11 =====================
story.append(PageBreak())
section('SECTION 11: TECHNICAL DEEP-DIVE QUESTIONS')

qa(47, 'Explain Bresenham\'s algorithm and why integer arithmetic matters.',
   'Computes discrete cells approximating a straight line using ONLY integer addition/subtraction.\n\n'
   'Steps along major axis, maintains error term, adjusts minor axis when error exceeds 0.5.\n\n'
   '<b>Why integer:</b> Faster than floating-point (especially embedded systems). Deterministic (no rounding errors). Output is discrete grid cells -- maps directly to grid representation. Runs in O(L) time.')

qa(48, 'What is Chebyshev distance and why use it?',
   'd(a,b) = max(|a_x - b_x|, |a_y - b_y|)\n\n'
   'Measures minimum king-moves on a chessboard. On 8-connected grids, minimum steps from a to b equals Chebyshev distance. Corridor boundary becomes a square band -- aligns with grid structure, efficient to compute. For 4-connected grids, Manhattan distance used instead.')

qa(49, 'Detail the ablation study results.',
   '<b>Radius (r_min, r_max):</b> (1,5): 94.3% opt, 8.2ms. (2,10): 99.8% opt, 10.3ms. (2,15): 100% opt, 12.1ms. Default balances both.\n\n'
   '<b>Window omega:</b> 3x3: 45.2%. 5x5: 58.4%. 7x7: 62.2% (best). 9x9: 61.8%. 11x11: 59.1%. Classic bias-variance.\n\n'
   '<b>Alpha:</b> 0.5: 96.8%. 1.0: 98.7% (best). 1.5: 97.2%. 2.0: 93.4%.\n\n'
   '<b>Strategy:</b> Base: 35.2%/89.4%. Standard: 55.8%/96.7%. Predictive: 62.2%/99.8% (winner).')

qa(50, 'What is Cohen\'s d and why is it important?',
   'd = (mean1 - mean2) / pooled_std. Measures PRACTICAL significance.\n\n'
   '|d|&lt;0.2: negligible. 0.2-0.5: small. 0.5-0.8: medium. &gt;=0.8: large.\n\n'
   'With large samples, tiny differences become statistically significant (p&lt;0.05). Cohen\'s d tells you if the difference MATTERS. AILS-Base vs A*: d=0.82 (large, practically meaningful).')

# ===================== SECTION 12 =====================
story.append(PageBreak())
section('SECTION 12: BROADER &amp; PHILOSOPHICAL QUESTIONS')

qa(51, 'What have you learned from doing this PhD?',
   '1. <b>Simple ideas can be powerful:</b> The corridor concept is conceptually simple but remarkably effective.\n'
   '2. <b>Rigorous evaluation matters:</b> The difference between "seems to work" and "here is exactly how much" is what makes a contribution.\n'
   '3. <b>Knowing limitations is valuable:</b> Characterizing failures is as important as showing successes.\n'
   '4. <b>Complementary methods beat silver bullets:</b> ILS and AILS are additions to the toolbox, not replacements.')

qa(52, 'If you could start over, what would you do differently?',
   '1. Start with C++ from the beginning\n'
   '2. Include Moving AI benchmarks from the start\n'
   '3. Unified hardware platform\n'
   '4. Explore D* Lite combination earlier\n'
   '5. More real-world data alongside synthetic\n\n'
   'That said, the research trajectory made sense: ILS first (proof of concept), then AILS (extension), then analysis.')

qa(53, 'How would you explain your thesis to a non-technical person?',
   'Imagine driving from home to the airport. You could explore every street in the city -- or you could focus on roads roughly in the airport\'s direction.\n\n'
   'My thesis does the same for robots: draw a straight line from A to B, only look at a narrow band around it. This makes pathfinding ~87% faster. If the band is too narrow, it automatically widens.\n\n'
   'My second innovation makes the band smart: wider near obstacles, narrow in open space.')

# ===================== SECTION 13 =====================
story.append(PageBreak())
section('SECTION 13: RAPID-FIRE QUESTIONS')

qa(54, 'What is the single most important result?',
   'ILS achieving 87.31% average execution time reduction across five algorithms while preserving path optimality. This demonstrates the core contribution: corridor-based restriction is simple, general, and dramatically effective.')

qa(55, 'What contribution will still matter in 10 years?',
   'The IDEA that corridor restriction can be applied as a general-purpose wrapper around ANY search algorithm. Specific algorithms evolve, but the principle of confining search to a geometrically motivated subspace is a lasting conceptual contribution.')

qa(56, 'If a referee disagrees with your biosecurity framing?',
   'The biosecurity framing is MOTIVATIONAL, not experimental. The algorithms are general-purpose grid-based pathfinding methods. The technical contribution stands independently of the application context.')

qa(57, 'What is the failure mode?',
   'REPEATED CORRIDOR EXPANSION on environments where optimal path deviates far from the Bresenham line. The algorithm never produces a WRONG answer, but it can be very slow (116x for room patterns). It always finds a valid path or correctly reports no path exists.')

qa(58, 'How do you ensure reproducibility?',
   '1. Fixed random seeds (documented in logs)\n'
   '2. Deterministic algorithms\n'
   '3. Median of three timing runs\n'
   '4. Explicit hardware/software specs\n'
   '5. Standardized 9-step preprocessing pipeline')

qa(59, 'Practical deployment path?',
   'Step 1: C++ reimplementation. Step 2: Moving AI validation. Step 3: ROS integration. Step 4: Gazebo/AirSim simulation. Step 5: Field trials on robots/drones. Step 6: D* Lite integration for dynamic replanning.')

qa(60, 'Summarize your thesis in one sentence.',
   'I developed two corridor-based pathfinding techniques -- ILS and AILS -- that dramatically reduce computation for grid-based navigation by confining search to a narrow, optionally density-adaptive band around the straight line between start and goal, achieving up to 87% time reduction while preserving path quality.')

doc.build(story)
print("PDF generated successfully at /home/user/phd/Viva_Preparation_QA_Guide.pdf")
