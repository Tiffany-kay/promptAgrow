// Backend Connection Test
async function testBackendConnection() {
    console.log('🧪 Testing backend connection...');
    
    try {
        // Test basic connectivity
        const response = await fetch(`${window.CONFIG.API.BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Backend connected successfully:', data);
            return true;
        } else {
            console.log('❌ Backend responded with error:', response.status);
            return false;
        }
    } catch (error) {
        console.log('❌ Cannot connect to backend:', error.message);
        console.log('💡 Make sure your backend is running on:', window.CONFIG.API.BASE_URL);
        return false;
    }
}

// Test file upload endpoint
async function testFileUpload() {
    console.log('📎 Testing file upload endpoint...');
    
    try {
        // Create a small test image file
        const canvas = document.createElement('canvas');
        canvas.width = 100;
        canvas.height = 100;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#2E7D32';
        ctx.fillRect(0, 0, 100, 100);
        
        // Convert to blob
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
        
        // Create form data
        const formData = new FormData();
        formData.append('image', blob, 'test.png');
        formData.append('productName', 'Test Product');
        formData.append('language', 'en');
        
        const response = await fetch(`${window.CONFIG.API.BASE_URL}/test-upload`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ File upload test successful:', data);
            return true;
        } else {
            console.log('❌ File upload test failed:', response.status);
            return false;
        }
    } catch (error) {
        console.log('❌ File upload test error:', error.message);
        return false;
    }
}

// Run tests on page load (only in debug mode)
if (window.CONFIG?.FEATURES?.DEBUG) {
    document.addEventListener('DOMContentLoaded', async () => {
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for app to load
        
        console.log('🚀 Running backend integration tests...');
        
        const connectionTest = await testBackendConnection();
        if (connectionTest) {
            await testFileUpload();
        }
        
        console.log('✨ Backend tests completed');
    });
}

// Expose test functions globally for manual testing
window.testBackend = {
    connection: testBackendConnection,
    upload: testFileUpload
};
