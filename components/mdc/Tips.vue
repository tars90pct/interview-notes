<template>
  <div
    class="w-full border-l border-primary px-2 py-1"
    style="background-color: #f3fbfc; border-left-width: 4px; border-color: forestgreen"
  >
    <slot />
  </div>
</template>
<script lang="ts">
  import { buildDefineComponentSetup } from "~/utils/internal";
  import { defineComponent, onMounted } from "vue";

  export default defineComponent({
    components: {},

    setup(props) {
      onMounted(() => {
        console.log(props);
      });
      const themeSelection = {
        info: [],
        warning: [],
      };

      return buildDefineComponentSetup(
        {
          data: {},
          methods: {},
          stores: {},
        },
        {}
      );
    },
  });
</script>
