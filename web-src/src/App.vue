<template>
  <q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer"/>

        <q-toolbar-title>
          <q-avatar>
            <img src="/img.png" alt="Logo">
          </q-avatar>
          Electron App
        </q-toolbar-title>


        <q-toggle
          v-model="darkMode"
          color="dark"
          dense
          icon="dark_mode"
          checked-icon="light_mode"
        />
      </q-toolbar>
    </q-header>

    <q-drawer
      show-if-above
      v-model="leftDrawerOpen"
      side="left"
      bordered
      behavior="mobile"
    >
      <q-scroll-area class="fit">
        <q-list padding>
          <!-- App Header -->
          <q-item class="q-pb-md">
            <q-item-section>
              <div class="flex items-center">
                <q-avatar size="28px">
                  <img src="/img.png" alt="Logo">
                </q-avatar>
                <span class="text-h6 q-ml-sm">Electron App</span>
              </div>
            </q-item-section>
          </q-item>

          <q-separator />

          <!-- Navigation Items -->
          <q-item-label header class="text-weight-bold q-mt-md">Main Navigation</q-item-label>

          <q-item clickable v-ripple to="/editor" exact active-class="bg-primary text-white">
            <q-item-section avatar>
              <q-icon name="mdi-matrix" />
            </q-item-section>
            <q-item-section>Main</q-item-section>
          </q-item>

          <q-separator spaced />

          <!-- Settings Item - Fixed at bottom -->
          <q-item-label header class="text-weight-bold">System</q-item-label>

          <q-item clickable v-ripple to="/settings" exact active-class="bg-primary text-white">
            <q-item-section avatar>
              <q-icon name="settings" />
            </q-item-section>
            <q-item-section>Settings</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="toggleDarkMode">
            <q-item-section avatar>
              <q-icon :name="darkMode ? 'light_mode' : 'dark_mode'" />
            </q-item-section>
            <q-item-section>{{ darkMode ? 'Light Mode' : 'Dark Mode' }}</q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>


    <q-page-container>
      <router-view/>
    </q-page-container>

  </q-layout>
</template>


<script>
import {ref, watch} from 'vue'
import { useQuasar } from "quasar";


export default {
  name: 'App',
  setup() {
    const leftDrawerOpen = ref(false)
    const $q = useQuasar()
    const darkMode = ref($q.dark.isActive)



    $q.dark.set($q.platform.is.desktop ? $q.dark.isActive : false)

    function toggleDarkMode() {
      darkMode.value = !darkMode.value
      // $q.dark.toggle()
    }
    watch(darkMode, (val) => {
      $q.dark.set(val)
      // Force a DOM update to ensure all components respond
      document.body.classList.toggle('body--dark', val)
    })


    function toggleLeftDrawer() {
      leftDrawerOpen.value = !leftDrawerOpen.value
    }


    window.addEventListener('load', function() {
      // Wait a moment to ensure everything is truly loaded
      setTimeout(function() {
        // Call the Python function to indicate UI is ready
        eel.on_ready();
      }, 500);
    });



    return {
      leftDrawerOpen,
      toggleLeftDrawer,
      toggleDarkMode,
      darkMode,
    }
  }
}
</script>

<style lang="scss">
.q-drawer {
  background-color: #f8f8f8;

  .q-item {
    border-radius: 8px;
    margin: 2px 0;
  }

  .q-item--active {
    font-weight: 500;

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 4px;
      border-radius: 0 4px 4px 0;
      background-color: var(--q-primary);
    }
  }
}

// Dark mode styles
.body--dark {
  .q-drawer {
    background-color: #1e1e1e;
  }
}


</style>

