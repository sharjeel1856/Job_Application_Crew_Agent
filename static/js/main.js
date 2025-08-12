// DOM Elements
const form = document.getElementById('jobForm');
const progressModal = document.getElementById('progressModal');
const submitBtn = document.getElementById('submitBtn');
const btnText = submitBtn.querySelector('.btn-text');
const btnLoading = submitBtn.querySelector('.btn-loading');

// Radio button elements
const resumeFileRadio = document.getElementById('resume_file_radio');
const resumeTextRadio = document.getElementById('resume_text_radio');
const linkedinFileRadio = document.getElementById('linkedin_file_radio');
const linkedinTextRadio = document.getElementById('linkedin_text_radio');

// Input sections
const resumeFileInput = document.getElementById('resume_file_input');
const resumeTextInput = document.getElementById('resume_text_input');
const linkedinFileInput = document.getElementById('linkedin_file_input');
const linkedinTextInput = document.getElementById('linkedin_text_input');

// Progress bars
const step1Progress = document.getElementById('step1-progress');
const step2Progress = document.getElementById('step2-progress');
const step3Progress = document.getElementById('step3-progress');
const step4Progress = document.getElementById('step4-progress');

// Radio button event listeners
resumeFileRadio.addEventListener('change', function() {
    if (this.checked) {
        resumeFileInput.style.display = 'block';
        resumeTextInput.style.display = 'none';
    }
});

resumeTextRadio.addEventListener('change', function() {
    if (this.checked) {
        resumeFileInput.style.display = 'none';
        resumeTextInput.style.display = 'block';
    }
});

linkedinFileRadio.addEventListener('change', function() {
    if (this.checked) {
        linkedinFileInput.style.display = 'block';
        linkedinTextInput.style.display = 'none';
    }
});

linkedinTextRadio.addEventListener('change', function() {
    if (this.checked) {
        linkedinFileInput.style.display = 'none';
        linkedinTextInput.style.display = 'block';
    }
});

// Form validation
function validateForm() {
    const jobUrl = document.getElementById('job_url').value;
    const githubUrl = document.getElementById('github_url').value;
    const linkedinUrl = document.getElementById('linkedin_url').value;
    
    // Check required URLs
    if (!jobUrl || !githubUrl || !linkedinUrl) {
        showError('Please fill in all required URL fields.');
        return false;
    }
    
    // Validate URLs
    const urlPattern = /^https?:\/\/.+/;
    if (!urlPattern.test(jobUrl) || !urlPattern.test(githubUrl) || !urlPattern.test(linkedinUrl)) {
        showError('Please enter valid URLs starting with http:// or https://');
        return false;
    }
    
    // Check resume input
    const resumeType = document.querySelector('input[name="resume_type"]:checked').value;
    if (resumeType === 'file') {
        const resumeFile = document.getElementById('resume_file').files[0];
        if (!resumeFile) {
            showError('Please select a resume file.');
            return false;
        }
        if (resumeFile.size > 5 * 1024 * 1024) { // 5MB limit
            showError('Resume file size must be less than 5MB.');
            return false;
        }
    } else {
        const resumeContent = document.getElementById('resume_content').value.trim();
        if (!resumeContent) {
            showError('Please paste your resume content.');
            return false;
        }
    }
    
    // Check LinkedIn input
    const linkedinType = document.querySelector('input[name="linkedin_type"]:checked').value;
    if (linkedinType === 'file') {
        const linkedinFile = document.getElementById('linkedin_file').files[0];
        if (linkedinFile && linkedinFile.size > 2 * 1024 * 1024) { // 2MB limit
            showError('LinkedIn file size must be less than 2MB.');
            return false;
        }
    }
    
    return true;
}

// Show error message
function showError(message) {
    // Remove existing error messages
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Create new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        background: #fed7d7;
        color: #e53e3e;
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #feb2b2;
    `;
    
    // Insert error message before the form
    form.parentNode.insertBefore(errorDiv, form);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

// Show progress modal
function showProgressModal() {
    progressModal.style.display = 'flex';
    startProgressAnimation();
}

// Hide progress modal
function hideProgressModal() {
    progressModal.style.display = 'none';
}

// Progress animation
function startProgressAnimation() {
    const steps = [step1Progress, step2Progress, step3Progress, step4Progress];
    const delays = [1000, 3000, 5000, 7000]; // 1s, 3s, 5s, 7s
    
    steps.forEach((step, index) => {
        setTimeout(() => {
            step.style.width = '100%';
            step.parentElement.parentElement.querySelector('.step-icon').style.background = '#667eea';
        }, delays[index]);
    });
}

// Form submission
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (!validateForm()) {
        return;
    }
    
    // Show loading state
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    
    // Show progress modal
    showProgressModal();
    
    try {
        // Create FormData
        const formData = new FormData();
        
        // Add URLs
        formData.append('job_url', document.getElementById('job_url').value);
        formData.append('github_url', document.getElementById('github_url').value);
        formData.append('linkedin_url', document.getElementById('linkedin_url').value);
        
        // Add resume data
        const resumeType = document.querySelector('input[name="resume_type"]:checked').value;
        formData.append('resume_type', resumeType);
        
        if (resumeType === 'file') {
            const resumeFile = document.getElementById('resume_file').files[0];
            formData.append('resume_file', resumeFile);
        } else {
            const resumeContent = document.getElementById('resume_content').value;
            formData.append('resume_content', resumeContent);
        }
        
        // Add LinkedIn data
        const linkedinType = document.querySelector('input[name="linkedin_type"]:checked').value;
        formData.append('linkedin_type', linkedinType);
        
        if (linkedinType === 'file') {
            const linkedinFile = document.getElementById('linkedin_file').files[0];
            if (linkedinFile) {
                formData.append('linkedin_file', linkedinFile);
            }
        } else {
            const linkedinContent = document.getElementById('linkedin_content').value;
            formData.append('linkedin_content', linkedinContent);
        }
        
        // Send request to backend
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            // Wait for progress animation to complete
            setTimeout(() => {
                hideProgressModal();
                // Redirect to results page
                if (result.redirect) {
                    window.location.href = result.redirect;
                } else {
                    alert('Analysis completed successfully! Check the generated files.');
                }
            }, 8000);
        } else {
            throw new Error(result.message || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Error:', error);
        hideProgressModal();
        showError('An error occurred during analysis. Please try again.');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
});

// File input change handlers
document.getElementById('resume_file').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        // Show file name
        const fileName = file.name;
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        this.nextElementSibling.textContent = `Selected: ${fileName} (${fileSize} MB)`;
    }
});

document.getElementById('linkedin_file').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        // Show file name
        const fileName = file.name;
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        this.nextElementSibling.textContent = `Selected: ${fileName} (${fileSize} MB)`;
    }
});

// Initialize form state
document.addEventListener('DOMContentLoaded', function() {
    // Set initial state
    resumeTextRadio.checked = true;
    linkedinTextRadio.checked = true;
    
    // Show/hide sections based on initial state
    resumeFileInput.style.display = 'none';
    resumeTextInput.style.display = 'block';
    linkedinFileInput.style.display = 'none';
    linkedinTextInput.style.display = 'block';
});
