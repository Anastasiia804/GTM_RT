<template>
  <div class="container-code">
    <div class="code-header">
      <h4>Container Code</h4>
      <button @click="copyCode" class="primary">
        {{ copied ? '✓ Copied!' : '📋 Copy Code' }}
      </button>
    </div>
    <pre><code>{{ code }}</code></pre>
  </div>
</template>

<script>
export default {
  name: 'ContainerCode',
  props: {
    code: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      copied: false
    }
  },
  methods: {
    async copyCode() {
      try {
        await navigator.clipboard.writeText(this.code)
        this.copied = true
        setTimeout(() => {
          this.copied = false
        }, 2000)
      } catch (err) {
        console.error('Failed to copy:', err)
      }
    }
  }
}
</script>

<style scoped>
.container-code {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 15px;
  margin: 20px 0;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.code-header h4 {
  margin: 0;
}

pre {
  background: #2c3e50;
  color: #ecf0f1;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  margin: 0;
}

code {
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.5;
}
</style>
