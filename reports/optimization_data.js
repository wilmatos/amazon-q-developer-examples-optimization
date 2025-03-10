// Benchmark data
const benchmarkData = {
    // Time comparison (in seconds)
    time: {
        original: 2.62,
        optimized: 1.01,
        improvement: 61.5
    },
    
    // CPU usage (in seconds)
    cpu: {
        original: 2.20,
        optimized: 1.37,
        improvement: 37.7
    },
    
    // Memory usage (in MB)
    memory: {
        original: 0.04,
        optimized: 34.63,
        change: -86475.0 // Negative indicates increased usage
    },
    
    // Detailed benchmark results
    detailedResults: [
        {
            name: "Iteration 1",
            original: {
                time: 2.15,
                memory: 0.12,
                cpu: 2.07
            },
            optimized: {
                time: 1.09,
                memory: 55.88,
                cpu: 1.34
            }
        },
        {
            name: "Iteration 2",
            original: {
                time: 3.43,
                memory: 0.00,
                cpu: 2.47
            },
            optimized: {
                time: 0.94,
                memory: 13.38,
                cpu: 1.40
            }
        },
        {
            name: "Iteration 3",
            original: {
                time: 2.28,
                memory: 0.00,
                cpu: 2.05
            },
            optimized: {
                time: 1.00,
                memory: 34.63,
                cpu: 1.37
            }
        }
    ],
    
    // Optimization techniques applied
    optimizationTechniques: [
        "Eliminated redundant I/O operations",
        "Implemented parallel processing",
        "Added format optimization",
        "Implemented caching with lru_cache",
        "Applied batch processing of transformations"
    ]
};