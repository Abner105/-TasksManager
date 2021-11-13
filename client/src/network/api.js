// 封装请求API
import request from "./request.js";
// 获取任务列表
export function getTasks(id){
  return request({
    url:'/gettasks',
    method:'post',
    data:{
      id
    }
  })
}
// 添加项目
export function addProject(name){
  return request({
    url:'/addproject',
    method:'post',
    data:{
      name
    }
  })
}
// 获取项目列表
export function getProjects(){
  return request({
    url:'/getprojects',
    method: "post",
  })
}
// 删除项目
export function delProject(id){
  return request({
    url:"/delproject",
    method:"post",
    data:{
      id
    }
  })
}
// 修改项目
export function alterProject(id,name){
  return request({
    url:'/alterproject',
    method:'post',
    data:{
      id,
      name
    }
  })
}
// 添加任务
export function addTask(title,pid){
  return request({
    url:'/addtask',
    method:"post",
    data:{
      title,
      pid
    }
  })
}
// 完成任务
export function done(id,pid){
  return request({
    url:'/done',
    method:"post",
    data:{
      id,
      pid
    }
  })
}
// 删除任务
export function delTask(id){
  return request({
    url:"/deltask",
    method:'post',
    data:{
      id
    }
  })
}
// 置顶任务
export function topTask(id,pid){
  return request({
    url:'/toptask',
    method:'post',
    data:{
      id,
      pid
    }
  })
}
// 修改任务 
export function alterTask(id,title){
  return request({
    url:"/altertask",
    method:"post",
    data:{
      id,
      title
    }
  })
}
