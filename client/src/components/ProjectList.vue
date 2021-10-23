<template>
  <div class="projects">
    <h2>项目列表</h2>
    <div v-for="project in sprojects" :key="project.id">
      <input
        type="text"
        :value="project.name"
        v-show="isalter == true && project.id == spid"
        v-focus="focusstatus"
        id="input"
        @blur="alterproject(project.name, $event)"
        @keyup.enter="alterproject(project.name, $event)"
      />
      <button
        v-show="!isalter || project.id != spid"
        :class="{ active: project.id == spid }"
        @click="switchProject(project.id)"
      >
        {{ project.name }}
      </button>
      <button v-show="project.id == spid" @click="getinput">修改</button>
      <button @click="delproject(project.id)">删除</button>
    </div>
    <!-- 引入弹窗组件，并监听弹窗中的确定事件 -->
    <alert-pane
      @itemclick="fclick"
      :btntext="'+添加项目'"
      :hint="'请输入项目名称'"
    ></alert-pane>
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
    fpid: {
      type: Number,
      default: 1,
    },
  },
  data() {
    return {
      sprojects: this.projects,
      spid: this.fpid,
      isalter: false,
      focusstatus: false,
    };
  },
  watch: {
    projects(val) {
      this.sprojects = val;
    },
    fpid(val) {
      this.spid = val;
    },
  },
  methods: {
    // 切换项目
    switchProject(pid) {
      this.spid = pid;
      this.$emit("refresh", this.spid);
    },
    // 添加项目并刷新项目列表
    fclick(name) {
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/addproject",
        data: { name },
      }).then((res) => {
        this.spid = res.data[0]["id"];
        this.$emit("refresh", this.spid);
        axios({
          method: "post",
          url: "http://127.0.0.1:5000/getprojects",
        }).then((res) => {
          this.sprojects = res.data;
        });
      });
    },
    // 删除项目
    delproject(pid) {
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/delproject",
        data: { id: pid },
      }).then(() => {
        axios({
          method: "post",
          url: "http://127.0.0.1:5000/getprojects",
        }).then((res) => {
          this.sprojects = res.data;
          if (this.spid == pid) {
            if (res.data[0]) {
              this.spid = res.data[0]["id"];
              this.$emit("refresh", this.spid);
            }else{
              this.spid = 0;
              this.$emit("refresh", this.spid);
            }
          }
        });
      });
    },
    // 点击修改按钮
    getinput() {
      this.isalter = true;
      this.focusstatus = true;
      const obj = document.getElementById("input");
      obj.selectionStart = obj.value.length;
      obj.selectionEnd = obj.value.length;
    },
    // 失去焦点修改项目名称
    alterproject(p, e) {
      this.focusstatus = false;
      this.isalter = false;
      if (p != e.target.value) {
        axios({
          method: "post",
          url: "http://127.0.0.1:5000/alterproject",
          data: { id: this.spid, name: e.target.value },
        }).then(() => {
          axios({
            method: "post",
            url: "http://127.0.0.1:5000/getprojects",
          }).then((res) => {
            this.sprojects = res.data;
          });
        });
      }
    },
  },
  directives: {
    focus: {
      update: function (el, { value }) {
        if (value) {
          el.focus();
        }
      },
    },
  },
};
</script>

<style scoped>
.active {
  background-color: aquamarine;
}
</style>
