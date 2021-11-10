<!-- This component shows error messages from an Axios request -->
<template>
  <div class="container text-center">
    <p class="error-header"><b>An error occurred: </b>{{ statusCodePar }}</p>
    <p>
      Type: {{ errorType }}<br /><i class="error-message">
        {{ errorMessage }}</i
      >
    </p>
  </div>
</template>

<script>
export default {
  name: "StatusBox.vue",
  props: {
    axiosError: {
      type: Object,
      required: true,
    },
  },
  computed: {
    statusCode() {
      if (!this.axiosError) {
        return "";
      }
      if (
        this.axiosError.response &&
        this.axiosError.response.status &&
        this.axiosError.response.status !== 200
      ) {
        return this.axiosError.response.status;
      }
      return "";
    },
    statusCodePar() {
      if (this.statusCode) {
        return `(${this.statusCode})`;
      }
      return "";
    },
    errorType() {
      if (this.axiosError.response && this.axiosError.response.status !== 200) {
        return "Response error";
      } else if (this.axiosError.request) {
        return "Request error";
      } else if (this.axiosError.message) {
        return "Other error";
      }
      return "";
    },
    errorMessage() {
      if (!this.axiosError) {
        return "";
      }
      if (this.axiosError.response) {
        let statusCode = this.axiosError.response.status;
        switch (true) {
          case statusCode === 200:
            return "";
          case statusCode === 422:
            return "Form validation error";
          case statusCode >= 500:
            return "Server error";
          default:
            return `Unhandled error code: ${statusCode}`;
        }
      } else if (this.axiosError.request) {
        return this.axiosError.request;
      } else {
        return this.axiosError.message;
      }
    },
  },
};
</script>

<style scoped>
.error-header {
  color: #ac2925;
}
.error-message {
  color: #5e5e5e;
}
</style>
