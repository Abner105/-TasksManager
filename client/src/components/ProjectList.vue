<template>
  <div class="projects">
    <div v-for="project in p" :key="project.id">
      <input type="text" :value="project.name" />
      <button>删除</button>
    </div>
    <!-- 引入弹窗组件，并监听弹窗中的确定事件 -->
    <alert-pane @itemclick="fclick"></alert-pane>
  </div>
</template>

<script>
import AlertPane from "./AlertPane.vue";
import axios from "axios";
export default {
  name: "ProjectList",
  components: {
    AlertPane,
  },
  // 接收父组件的数据
  props: {
    projects: {
      type: Array,
      default() {
        return ["暂无数据"];
      },
    },
  },
  data() {
    return {
      p: this.projects,
    };
  },
  watch: {
    projects(val) {
      this.p = val;
    },
  },
  methods: {
    // 添加项目并刷新项目列表
    fclick(name) {
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/addproject",
        data: { name },
      }).then(() => {
        axios({
          method: "post",
          url: "http://127.0.0.1:5000/getprojects",
        }).then((res) => {
          // 向父组件中传递刷新后的项目列表
          this.$emit("addproject", res.data);
        });
      });
    },
  },
};
</script>

<style scoped>
</style>
