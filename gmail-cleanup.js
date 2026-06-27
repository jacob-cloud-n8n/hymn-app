/**
 * Gmail 批次清理 + 自動分類腳本
 * 
 * 使用方法：
 * 1. 打開 https://script.google.com
 * 2. 新建專案 → 貼上這個腳本
 * 3. 先點「選單」列上的 run → 選 setup → 授權
 * 4. 點 authorizeCleanup → 執行清理
 */

// ============================================================
// 設定區：依你的需求修改
// ============================================================

const CONFIG = {
  // 超過 2 年的郵件 → 刪除
  deleteOlderThanYears: 2,
  // 1-2 年的郵件 → 封存
  archiveOlderThanYears: 1,
  
  // 分類標籤設定
  labels: [
    { name: '01-緊急/需立即回覆', color: '#ff0000' },
    { name: '02-團隊/AI溝通', color: '#4285f4' },
    { name: '03-客戶專案', color: '#34a853' },
    { name: '04-系統通知/自動', color: '#fbbc04' },
    { name: '05-一般/可稍後', color: '#a0a0a0' },
  ],

  // 緊急關鍵字（寄件者或主旨包含這些 → 標記 01-緊急）
  urgentPatterns: ['urgent', '緊急', 'payment', '付款', 'down', 'crash', 'error', '500'],

  // 團隊寄件者
  teamSenders: ['codex', 'hermes', 'antigravity', 'opencode', 'mimocode', 'claude', 'n8n', 'anti-gravity'],

  // 客戶專案關鍵字
  clientKeywords: ['美地', '琢石', '羊奶', 'STAR', '書僮', '課程', '客戶', 'client', 'invoice', '合約', '報價'],

  // 系統通知寄件者
  systemSenders: ['noreply', 'no-reply', 'notification', 'github', 'zeabur', 'firebase', 'google', 'notion', 'telegram', 'discord', '@google.com', '@github.com', '@firebase.com'],
};

// ============================================================
// 主程式：建立標籤
// ============================================================

function setup() {
  Logger.log('=== 建立標籤 ===');
  CONFIG.labels.forEach(function(label) {
    try {
      GmailApp.createLabel(label.name);
      Logger.log('建立標籤: ' + label.name);
    } catch(e) {
      Logger.log('標籤已存在: ' + label.name);
    }
  });
  Logger.log('=== 完成 ===');
}

// ============================================================
// 主程式：清理舊信
// ============================================================

function authorizeCleanup() {
  var now = new Date();

  // 1. 刪除超過 2 年的信
  var deleteBefore = new Date(now);
  deleteBefore.setFullYear(now.getFullYear() - CONFIG.deleteOlderThanYears);
  Logger.log('=== 搜尋 ' + CONFIG.deleteOlderThanYears + ' 年前的郵件（將刪除）===');
  Logger.log('刪除線: before ' + formatDate(deleteBefore));
  
  var totalDeleted = 0;
  var batchSize = 100;

  var deleteQuery = 'before:' + formatDate(deleteBefore) + ' in:anywhere';
  while (true) {
    var threads = GmailApp.search(deleteQuery, 0, batchSize);
    if (threads.length === 0) break;
    Logger.log('刪除 ' + threads.length + ' 組郵件...');
    GmailApp.moveThreadsToTrash(threads);
    totalDeleted += threads.length;
    Utilities.sleep(1000); // 避免觸發 Gmail API 限流
  }
  Logger.log('已刪除: ' + totalDeleted + ' 組郵件');

  // 2. 封存 1-2 年之間的信
  var archiveBefore = new Date(now);
  archiveBefore.setFullYear(now.getFullYear() - CONFIG.archiveOlderThanYears);
  Logger.log('=== 搜尋 ' + CONFIG.archiveOlderThanYears + '-' + CONFIG.deleteOlderThanYears + ' 年前的郵件（將封存）===');
  Logger.log('範圍: before ' + formatDate(archiveBefore) + ' after ' + formatDate(deleteBefore));

  var totalArchived = 0;
  var archiveQuery = 'before:' + formatDate(archiveBefore) + ' after:' + formatDate(deleteBefore) + ' in:anywhere';
  while (true) {
    var threads = GmailApp.search(archiveQuery, 0, batchSize);
    if (threads.length === 0) break;
    Logger.log('封存 ' + threads.length + ' 組郵件...');
    GmailApp.moveThreadsToArchive(threads);
    totalArchived += threads.length;
    Utilities.sleep(1000);
  }
  Logger.log('已封存: ' + totalArchived + ' 組郵件');

  Logger.log('=== 清理完成 ===');
  Logger.log('刪除: ' + totalDeleted + ' | 封存: ' + totalArchived);
}

// ============================================================
// 主程式：自動分類（加標籤）
// ============================================================

function classifyAll() {
  Logger.log('=== 開始分類 ===');
  
  var now = new Date();
  var oneMonthAgo = new Date(now);
  oneMonthAgo.setMonth(now.getMonth() - 1);
  
  // 分 5 批處理，避免逾時
  var categories = [
    { label: '01-緊急/需立即回覆', patterns: CONFIG.urgentPatterns },
    { label: '02-團隊/AI溝通', patterns: CONFIG.teamSenders },
    { label: '03-客戶專案', patterns: CONFIG.clientKeywords },
    { label: '04-系統通知/自動', patterns: CONFIG.systemSenders },
  ];

  categories.forEach(function(cat) {
    var label = GmailApp.getUserLabelByName(cat.label);
    if (!label) {
      Logger.log('跳過（標籤不存在）: ' + cat.label);
      return;
    }
    
    cat.patterns.forEach(function(pattern) {
      var query = '(from:' + pattern + ' OR subject:' + pattern + ') -label:' + cat.label;
      while (true) {
        var threads = GmailApp.search(query, 0, 100);
        if (threads.length === 0) break;
        label.addToThreads(threads);
        Logger.log('分類: ' + cat.label + ' ← ' + threads.length + ' 組 (' + pattern + ')');
        Utilities.sleep(500);
      }
    });
  });

  Logger.log('=== 分類完成 ===');
}

function formatDate(date) {
  var y = date.getFullYear();
  var m = ('0' + (date.getMonth() + 1)).slice(-2);
  var d = ('0' + date.getDate()).slice(-2);
  return y + '/' + m + '/' + d;
}
