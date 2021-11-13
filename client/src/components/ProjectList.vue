<template>
  <div class="projects">
    <div class="logo">
      <img src="../assets/logo.png" alt="" />
      <span>Task Manager</span>
    </div>
    <div class="title">
      <h2>项目列表</h2>
      <!-- 引入弹窗组件，并监听弹窗中的确定事件 -->
      <alert-pane @itemclick="fclick" :hint="'请输入项目名称'"></alert-pane>
    </div>
    <div class="wrapper">
      <div
        v-for="project in sprojects"
        :key="project.id"
        :class="{ active: project.id == spid, item: true }"
      >
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
          @click="switchProject(project.id)"
          :title="project.name"
        >
          {{ project.name }}
        </button>
        <div
          @click="delproject(project.id)"
          class="iconfont icon-shanchu"
        ></div>
        <div
          v-show="project.id == spid"
          @click="getinput"
          class="iconfont icon-cangpeitubiao_xiugaixiugaiziliao"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
import AlertPane from "./AlertPane.vue";
import { addProject, getProjects,delProject,alterProject} from "../network/api.js";
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
      addProject(name).then((res) => {
        this.spid = res.data[0]["id"];
        this.$emit("refresh", this.spid);
        getProjects().then((res) => {
          this.$emit("getproject", res.data);
        });
      });
    },
    // 删除项目
    delproject(pid) {
      delProject(pid).then(() => {
        getProjects().then((res) => {
          this.$emit("getproject", res.data);
          // 解决bug：如果删除的项目刚好是选中的项目，默认选中的是第一个项目
          if (this.spid == pid) {
            if (res.data[0]) {
              this.spid = res.data[0]["id"];
              this.$emit("refresh", this.spid);
            } else {
              this.spid = 0;
              this.$emit("refresh", this.spid);
            }
          }
        });
      });
    },
    // 点击修改按钮后，显示输入框
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
        alterProject(this.spid,e.target.value).then(() => {
          getProjects().then((res) => {
            this.$emit("getproject", res.data);
          });
        });
      }
    },
  },
  // 自定义获取焦点属性
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
.projects {
  width: 280px;
  background-color: #ddd;
}
.logo {
  /* background-color: aquamarine; */
  width: 250px;
  height: 50px;
  padding: 30px 15px 10px;
}
.logo img {
  height: 100%;
}
.logo span {
  display: inline-block;
  color: #4cbae9;
  font-size: 24px;
  vertical-align: top;
  line-height: 50px;
  font-weight: 900;
}
.title {
  height: 50px;
  padding: 5px 20px 10px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  line-height: 50px;
}
.title h2 {
  font-size: 20px;
  font-weight: 600;
}
.item {
  display: block;
  height: 60px;
  padding: 0 15px;
  margin: 8px 2px;
}
.item:hover {
  background-color: rgb(247, 247, 247);
}
.item button,
.item input {
  display: inline-block;
  height: 60px;
  width: 175px;
  font-size: 16px;
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.item div {
  display: inline-block;
  font-size: 18px;
  height: 50px;
  width: 27px;
  line-height: 50px;
  text-align: center;
}
.item div:hover {
  color: #2ea5d8;
  font-weight: 900;
}
div.icon-shanchu:hover {
  color: rgb(255, 74, 74);
  font-weight: 900;
}
.wrapper {
  overflow-y: auto;
  width: 280px;
  height: 540px;
  /* background-color: antiquewhite; */
}
.active {
  background-color: rgb(247, 247, 247);
}
</style>
