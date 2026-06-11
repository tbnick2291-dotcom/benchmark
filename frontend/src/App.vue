<template>
  <el-container style="height: 100vh">
    <el-aside width="200px" style="background:#1e1e2e">
      <div style="color:#cdd6f4;padding:20px;font-size:16px;font-weight:bold">
        LLM Benchmark
      </div>
      <el-menu
        :default-active="$route.path"
        router
        background-color="#1e1e2e"
        text-color="#cdd6f4"
        active-text-color="#89b4fa"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Monitor /></el-icon>Dashboard
        </el-menu-item>
        <el-menu-item index="/models">
          <el-icon><Box /></el-icon>Models
        </el-menu-item>
        <el-menu-item index="/tasks">
          <el-icon><List /></el-icon>Tasks
        </el-menu-item>
        <el-menu-item index="/leaderboard">
          <el-icon><Trophy /></el-icon>Leaderboard
        </el-menu-item>
        <el-menu-item index="/reports">
          <el-icon><Document /></el-icon>Reports
        </el-menu-item>
        <el-menu-item index="/system">
          <el-icon><Setting /></el-icon>System
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { Monitor, Box, List, Trophy, Document, Setting } from '@element-plus/icons-vue'
</script>
