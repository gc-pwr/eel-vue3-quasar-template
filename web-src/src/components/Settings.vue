<template>
  <div class="q-pa-md">
    <q-card>
      <q-card-section class="bg-primary text-white">
        <div class="text-h6">
          <q-icon name="settings" class="q-mr-sm" /> Application Settings
        </div>
      </q-card-section>

      <!-- Loading state -->
      <div v-if="loading" class="q-pa-xl flex flex-center column">
        <q-spinner color="primary" size="3em" />
        <span class="q-mt-sm text-subtitle1">Loading settings...</span>
      </div>

      <!-- Settings form -->
      <q-form @submit="saveSettings" v-else>
        <q-card-section>
          <q-expansion-item
              expand-separator
              icon="home"
              label="General Settings"
              header-class="text-primary"
              default-opened
          >
            <q-card>
              <q-card-section>
                <!-- Theme Selection -->
                <div class="row q-col-gutter-md items-center q-mb-md">
                  <div class="col-12 col-md-6">
                    <q-select
                        v-model="formSettings.theme"
                        :options="themeOptions"
                        label="Theme"
                        filled
                        emit-value
                        map-options
                        class="q-mb-sm"
                    >
                      <template v-slot:prepend>
                        <q-icon name="palette" color="primary" />
                      </template>
                    </q-select>
                  </div>
                </div>

                <!-- Window Size Settings -->
                <div class="q-mb-md">
                  <div class="text-subtitle2 q-mb-sm q-pl-sm text-primary">
                    <q-icon name="aspect_ratio" class="q-mr-xs" /> Window Size
                  </div>
                  <div class="row q-col-gutter-md">
                    <div class="col-12 col-md-6">
                      <q-input
                          v-model.number="windowWidth"
                          type="number"
                          label="Width"
                          filled
                          min="400"
                          class="q-mb-sm"
                          :rules="[val => val >= 400 || 'Minimum width is 400px']"
                      >
                        <template v-slot:prepend>
                          <q-icon name="width" color="primary" />
                        </template>
                        <template v-slot:append>
                          <div class="text-caption">px</div>
                        </template>
                      </q-input>
                    </div>
                    <div class="col-12 col-md-6">
                      <q-input
                          v-model.number="windowHeight"
                          type="number"
                          label="Height"
                          filled
                          min="400"
                          class="q-mb-sm"
                          :rules="[val => val >= 400 || 'Minimum height is 400px']"
                      >
                        <template v-slot:prepend>
                          <q-icon name="height" color="primary" />
                        </template>
                        <template v-slot:append>
                          <div class="text-caption">px</div>
                        </template>
                      </q-input>
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </q-expansion-item>
        </q-card-section>

        <!-- Action Buttons -->
        <q-card-actions align="right" class="q-py-md">
          <q-btn
              type="button"
              label="Reset to Defaults"
              color="warning"
              flat
              icon="restart_alt"
              @click="resetToDefaults"
              class="q-mr-md"
          />
          <q-btn
              type="submit"
              label="Save Settings"
              color="primary"
              icon="save"
              :loading="saving"
          />
        </q-card-actions>
      </q-form>
    </q-card>

    <!-- Notifications -->
    <q-dialog v-model="showSuccessDialog">
      <q-card>
        <q-card-section class="row items-center bg-positive text-white">
          <q-avatar icon="check_circle" text-color="white" />
          <span class="q-ml-sm text-h6">Success</span>
        </q-card-section>
        <q-card-section class="q-pt-md">
          Settings saved successfully!
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useQuasar } from 'quasar';

const $q = useQuasar();

// Reactive state
const loading = ref(true);
const saving = ref(false);
const showSuccessDialog = ref(false);
const formSettings = reactive({
  output_dir: '',
  theme: 'light',
  window_size: [700, 680]
});

const windowWidth = ref(700);
const windowHeight = ref(680);

const themeOptions = [
  { label: 'Light', value: 'light' },
  { label: 'Dark', value: 'dark' }
];

// Load settings when component is mounted
onMounted(() => {
  loadSettings();
});

// Methods
const loadSettings = async () => {
  loading.value = true;
  try {
    // Call the Python backend to get settings
    const settings = await window.eel.get_user_settings()();

    // Update formSettings with values from backend
    Object.assign(formSettings, settings);

    // Handle window size which is stored as a tuple
    if (Array.isArray(settings.window_size)) {
      windowWidth.value = settings.window_size[0];
      windowHeight.value = settings.window_size[1];
    }
  } catch (error) {
    console.error('Error loading settings:', error);
    $q.notify({
      color: 'negative',
      position: 'top',
      message: 'Failed to load settings',
      icon: 'error'
    });
  } finally {
    loading.value = false;
  }
};

const saveSettings = async () => {
  saving.value = true;
  try {
    // Update window size from separate inputs
    formSettings.window_size = [windowWidth.value, windowHeight.value];

    // Call the Python backend to save settings
    const result = await window.eel.save_user_settings(formSettings)();

    if (result.success) {
      showSuccessDialog.value = true;
    } else {
      throw new Error('Failed to save settings');
    }
  } catch (error) {
    console.error('Error saving settings:', error);
    $q.notify({
      color: 'negative',
      position: 'top',
      message: 'Failed to save settings',
      icon: 'error'
    });
  } finally {
    saving.value = false;
  }
};

const resetToDefaults = async () => {
  $q.dialog({
    title: 'Confirm Reset',
    message: 'Are you sure you want to reset all settings to their default values?',
    cancel: true,
    persistent: true
  }).onOk(async () => {
    loading.value = true;
    try {
      // Call a Python function to reset settings
      await window.eel.reset_settings()();
      // Reload settings
      await loadSettings();
      $q.notify({
        color: 'positive',
        position: 'top',
        message: 'Settings have been reset to defaults',
        icon: 'settings_backup_restore'
      });
    } catch (error) {
      console.error('Error resetting settings:', error);
      $q.notify({
        color: 'negative',
        position: 'top',
        message: 'Failed to reset settings',
        icon: 'error'
      });
    } finally {
      loading.value = false;
    }
  });
};


</script>

<style scoped>
</style>