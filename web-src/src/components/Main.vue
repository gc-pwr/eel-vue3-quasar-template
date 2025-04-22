<template>
  <div class="q-pa-md">
    <q-card class="welcome-card">
      <q-card-section class="bg-primary text-white">
        <div class="text-h4 q-mb-sm">Welcome to Your Quasar App</div>
        <div class="text-subtitle1">Start building amazing cross-platform applications</div>
      </q-card-section>

      <q-card-section class="q-py-lg">
        <div class="row items-center justify-center q-col-gutter-lg">
          <div class="col-12 col-md-6 text-center">
            <q-icon name="code" size="6rem" color="primary" class="q-mb-md" />
            <div class="text-h5 q-mb-sm">Ready to Code</div>
            <p class="text-body1">
              This template provides a solid foundation for your next project.
              Build with Electron, Python, Vue 3 and Quasar's powerful components.
            </p>
          </div>

          <div class="col-12 col-md-6">
            <q-list bordered separator class="rounded-borders">
              <q-item-label header class="text-primary text-h6">
                What will you create?
              </q-item-label>

              <q-item v-ripple clickable v-for="idea in projectIdeas" :key="idea.title">
                <q-item-section avatar>
                  <q-icon :name="idea.icon" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ idea.title }}</q-item-label>
                  <q-item-label caption>{{ idea.description }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </div>
      </q-card-section>

      <q-separator />

      <q-card-actions align="center" class="q-pa-md">
        <q-btn
            color="primary"
            label="Get Started"
            icon="rocket_launch"
            size="lg"
            @click="showStartMessage"
            unelevated
        />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
import { useQuasar } from 'quasar'
import { ref } from 'vue'

export default {
  name: 'Main',
  setup() {
    const $q = useQuasar()

    const projectIdeas = ref([
      {
        icon: 'terminal',
        title: 'System Monitoring Tool',
        description: 'Desktop app to monitor system resources with Python backend'
      },
      {
        icon: 'dashboard',
        title: 'Internal Admin Dashboard',
        description: 'Create powerful tools for managing company data and operations'
      },
      {
        icon: 'folder',
        title: 'File Management Utility',
        description: 'Build a desktop app to organize and process files efficiently'
      },
      {
        icon: 'analytics',
        title: 'Data Analysis Tool',
        description: 'Develop an application to visualize and analyze company data'
      }
    ])


    const showStartMessage = () => {
      $q.notify({
        message: 'Welcome to your new project! Let\'s build something amazing.',
        color: 'positive',
        icon: 'sentiment_very_satisfied',
        position: 'top',
        timeout: 2500
      })
    }

    return {
      projectIdeas,
      showStartMessage
    }
  }
}
</script>

<style scoped>
.welcome-card {
  max-width: 1000px;
  margin: 0 auto;
  transition: all 0.3s ease;
}

.welcome-card:hover {
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}

</style>