<template>
  <div class="projects">
      <div v-for="p in projects" :key="p.id">
        <input type="text" :value="p.name"/>
        <button>删除</button>
      </div>
      <button>添加项目</button>
  </div>
</template>

<script>
export default {
  name: "ProjectList",
  props: {
    projects: {
      type: Array,
      default() {
        return ["暂无数据"];
      },
    },
  },
};
</script>

<style scoped>

</style>
