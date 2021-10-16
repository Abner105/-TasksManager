<template>
  <div id="app">
    <select name="" id="" >
      <option v-for="project in projects" :key="project.id" :value="project.id">{{project.name}}</option>
    </select>
    <button>添加项目</button>
    <HelloWorld :tasks="tasks"/>
  </div>
</template>

<script>
import HelloWorld from './components/TaskList.vue'
export default {
  name: 'App',
  components: {
    HelloWorld
  },
  data(){
    return {
      projects:[
        {id:1,name:'项目1'},
        {id:2,name:'项目2'},
        {id:3,name:'项目3'},
      ],
      tasks:[
        {id:2,title:'逛公园',date:'10月13日',condition:'todo'},
        {id:1,title:'完成游戏',date:'10月12日',condition:'todo'},
        {id:3,title:'吃饭',date:'10月15日',condition:'done'},
        {id:4,title:'上王者',date:'10月16日',condition:'done'},
      ]
    }
  }
}
</script>

<style>
*{
  list-style: none;
  margin: 0;
  padding: 0;
  text-decoration: none;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
