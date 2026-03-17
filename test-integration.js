const db = require('./services/database');
const metricsService = require('./services/metricsService');
const AnalyticsService = require('./services/analytics');

async function runTests() {
let failed = false;
console.log('🚀 Starting Integration Tests...');

```
// Test 1: Database Connection & Schema
try {
    await new Promise((resolve, reject) => {
        db.get("SELECT name FROM sqlite_master WHERE type='table' AND name='users'", (err, row) => {
            if (err) return reject(err);
            if (!row) return reject(new Error('Table "users" not found'));
            console.log('✅ Base Database Schema verified');
            resolve();
        });
    });
} catch (e) {
    console.error('❌ Database Schema Test Failed:', e.message);
    failed = true;
}

// Test 2: Metrics Service
try {
    const dora = await metricsService.getDoraMetrics();
    if (typeof dora.successRate !== 'number') {
        throw new Error('Invalid successRate type');
    }
    console.log('✅ Metrics Service Integrity verified');
} catch (e) {
    console.error('❌ Metrics Service Test Failed:', e.message);
    failed = true;
}

// Test 3: Analytics Service
try {
    const analytics = new AnalyticsService();
    const quality = await analytics.getQualityMetrics(1);

    if (typeof quality.pass_rate !== 'number') {
        throw new Error('Invalid pass_rate type');
    }

    console.log('✅ Analytics Service Integrity verified');
} catch (e) {
    console.error('❌ Analytics Service Test Failed:', e.message);
    failed = true;
}

if (failed) {
    console.log('\n🔴 SOME TESTS FAILED');
    process.exit(1);
} else {
    console.log('\n🟢 ALL INTEGRATION TESTS PASSED');
    process.exit(0);
}
```

}

runTests().catch(err => {
console.error('FATAL TEST ERROR:', err);
process.exit(1);
});
