<template>
  <div></div>
</template>
<script lang="ts">
  import { buildDefineComponentSetup } from "~/utils/internal";
  import { defineComponent, onMounted } from "vue";

  export default defineComponent({
    components: {},
    props: {},
    setup(props) {
      definePageMeta({
        layout: "official-layout",
      });
      const router = useRouter();
      router.push("/getting-started");
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
