<template>
  <div></div>
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
        layout: false,
      });
      const question = ref("");
      const answer = ref("");
      watch(question, (newQuestion, oldQuestion) => {
        answer.value = newQuestion + oldQuestion;
      });
      onMounted(() => {
        console.log(props);
      });
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
