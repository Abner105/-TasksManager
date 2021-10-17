<template>
  <div class="tasks">
    <ul>
      <li v-for="task in tasks" :key="task.id" :class="task.condition">
        <div class="task">
          <h2>{{ task.title }}
          <button>完成</button>
          <button>修改</button>
          <button>删除</button></h2>
          <span>{{ task.date }}</span>
        </div>
      </li>
    </ul>
    <button>添加任务</button>
  </div>
</template>

<script>
export default {
  name: "TaskList",
  props: {
    tasks: {
      type: Array,
      default() {
        return ["暂无数据"];
      },
    },
  },
};
</script>

<style scoped>
.done {
  color: #ddd;
}
</style>
