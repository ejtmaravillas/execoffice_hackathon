<script setup>
import { ref } from "vue";
import axios from "axios";

// Reactive variables for file and its content
const fileContent = ref("");
const fileSummary = ref("");
const selectedFile = ref(null);
const isLoading = ref(false);

// Handle file selection and upload
const handleFileUpload = async (event) => {
  selectedFile.value = event.target.files[0];
  if (selectedFile.value) {
    const formData = new FormData();
    formData.append("file", selectedFile.value);

    try {
      isLoading.value = true; // Show loading state

      // Make API call to the backend
      const response = await axios.post(
        "http://172.29.67.197:5000/extract-and-summarize-pdf", // Backend endpoint
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      const { text, summary } = response.data;

      // Display extracted text and summary
      fileContent.value = text;
      fileSummary.value = summary;
    } catch (error) {
      console.error("Error uploading file:", error);
      fileContent.value = "An error occurred. Please try again.";
      fileSummary.value = "";
    } finally {
      isLoading.value = false; // Hide loading state
    }
  }
};
</script>

<template>
  <div class="flex items-center justify-center h-screen">
    <div class="bg-red-100 shadow-lg rounded-lg p-6 w-full max-w-4xl">
      <h1 class="text-2xl font-bold text-gray-800 mb-6 text-center">
        PDF Extract and Summarize
      </h1>
      <div class="mb-4">
        <label
          for="file-upload"
          class="block mb-2 text-lg font-medium text-gray-700"
        >
          Upload a PDF file:
        </label>
        <input
          id="file-upload"
          type="file"
          @change="handleFileUpload"
          class="block w-full text-sm text-gray-700 border border-gray-300 rounded-lg cursor-pointer focus:outline-none"
        />
      </div>

      <div v-if="selectedFile" class="mt-4 text-sm text-gray-700">
        <p><strong>File Name:</strong> {{ selectedFile.name }}</p>
        <p><strong>File Size:</strong> {{ (selectedFile.size / 1024).toFixed(2) }} KB</p>
        <p><strong>File Type:</strong> {{ selectedFile.type }}</p>
      </div>

      <div v-if="isLoading" class="text-center text-gray-500 mt-6">
        Processing the file, please wait...
      </div>

      <div
        v-if="fileContent && !isLoading"
        class="mt-8 bg-gray-100 border border-gray-300 rounded-lg p-6 max-h-screen overflow-auto"
      >
        <h2 class="mb-4 text-xl font-semibold text-gray-800">Extracted Text:</h2>
        <pre class="text-base text-gray-600 whitespace-pre-wrap mb-8">{{ fileContent }}</pre>

        <h2 class="mb-4 text-xl font-semibold text-gray-800">Summary:</h2>
        <pre class="text-base text-gray-600 whitespace-pre-wrap">{{ fileSummary }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Ensure the extracted content section is prominent */
pre {
  white-space: pre-wrap; /* Ensure long text wraps */
  word-wrap: break-word; /* Break words if needed */
}

.max-h-screen {
  max-height: 70vh; /* Set a maximum height for scrollable content */
}
</style>
