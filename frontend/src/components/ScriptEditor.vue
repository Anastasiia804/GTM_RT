<template>
  <div class="script-editor">
    <div class="form-group">
      <label>Script Name</label>
      <input v-model="localScript.name" type="text" placeholder="Enter script name" />
    </div>

    <div class="form-group">
      <label>Script Type</label>
      <select v-model="localScript.script_type">
        <option value="external">External URL</option>
        <option value="inline">Inline Code</option>
      </select>
    </div>

    <div class="form-group">
      <label>{{ localScript.script_type === 'external' ? 'Script URL' : 'Script Code' }}</label>
      <textarea
        v-model="localScript.content"
        :placeholder="localScript.script_type === 'external' ? 'https://example.com/script.js' : 'Enter JavaScript code'"
        rows="5"
      ></textarea>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label>Priority (lower = first)</label>
        <input v-model.number="localScript.priority" type="number" min="0" />
      </div>

      <div class="form-group checkbox">
        <label>
          <input v-model="localScript.is_enabled" type="checkbox" />
          Enabled
        </label>
      </div>

      <div class="form-group checkbox">
        <label>
          <input v-model="localScript.is_async" type="checkbox" />
          Async
        </label>
      </div>

      <div class="form-group checkbox">
        <label>
          <input v-model="localScript.is_defer" type="checkbox" />
          Defer
        </label>
      </div>
    </div>

    <div class="form-actions">
      <button @click="$emit('save', localScript)" class="primary">Save Script</button>
      <button @click="$emit('cancel')" class="secondary">Cancel</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScriptEditor',
  props: {
    script: {
      type: Object,
      default: () => ({
        name: '',
        script_type: 'external',
        content: '',
        is_enabled: true,
        priority: 0,
        is_async: true,
        is_defer: false
      })
    }
  },
  data() {
    return {
      localScript: { ...this.script }
    }
  },
  watch: {
    script: {
      handler(newVal) {
        this.localScript = { ...newVal }
      },
      deep: true
    }
  }
}
</script>

<style scoped>
.script-editor {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 15px;
}

.form-group.checkbox {
  display: flex;
  align-items: center;
}

.form-group.checkbox label {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 0;
}

.form-group.checkbox input[type="checkbox"] {
  width: auto;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}
</style>
