<template>
  <div class="rounded-sm bg-primary/5 px-2 py-1">
    <slot />
  </div>
</template>
<script lang="ts">
  import { buildDefineComponentSetup } from "~/utils/internal";
  import { defineComponent, onMounted } from "vue";

  export default defineComponent({
    components: {},
    props: {},
    setup(props) {
      onMounted(() => {});
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
