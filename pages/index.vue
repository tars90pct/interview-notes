<template>
  <div>index</div>
</template>
<script lang="ts">
  import { buildDefineComponentSetup } from "~/utils/internal";
  import { defineComponent, onMounted, ref, watch } from "vue";
  import type { NuxtError } from "#app";

  export default defineComponent({
    components: {},
    props: {
      error: {
        type: Object as () => NuxtError,
        default: () => {
          return {
            statusCode: 404,
          };
        },
      },
    },
    setup(props) {
      definePageMeta({
        layout: "official-layout",
      });
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
