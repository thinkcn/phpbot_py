"""
    Copyright (c) 2020, mll <coleflowersma at gmail dot com>
    All rights reserved.
"""
import os
import sublime
import sublime_plugin

# link: http://www.sublimetext.com/docs/3/api_reference.html#sublime.View
# command phpbot_gettersetter 
class PhpbotGettersetterCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        # 获取配置
        settings = sublime.load_settings('phpbot.sublime-settings')
        phpbot = settings.get("phpbot")
        if phpbot == None :
            phpbot = self.view.settings().get("phpbot")

        if phpbot == None:
            sublime.message_dialog('请配置有效的phpbot路径')
            return

        # 测试有效性
        versionCmd = phpbot + ' --version ' + ' 2>&1 '
        verPip = os.popen(versionCmd)
        version = verPip.read()
        if version == None or len(version) < 6 or version[0:6] != 'phpbot':
            sublime.message_dialog('请配置有效的phpbot路径.')
            return

        command = phpbot
        mark = ' -gs ' 
        file_path = self.view.file_name()
        v = self.view
        if not file_path:
            file_path = sublime.active_window().active_view().file_name() 
            v = sublime.active_window().active_view()
        if not file_path:
            sublime.message_dialog("请选择要操作的文件")
            return;
        # print(file_path)
        cmd = command + ' ' + file_path + mark 
        
        # 状态栏回显信息
        # self.view.window().status_message(cmd)
        # 
        # sublime.status_message("User said: " + cmd) 
        # 弹框
        # sublime.message_dialog("User said: " + cmd)
   
        # 
        # res = os.system(cmd)
        # print(res)

        p = os.popen(cmd)
        gs = p.read() 
        lastPos = self.findLastBracket(v)
        currPos = v.sel()[0].begin();
        if not currPos:
            currPos = lastPos
        print(currPos)
        v.insert(edit, currPos, gs)
        p.close()
    def findLastBracket(self, view):
        pos = 0
        lastPos = 1

        pos = view.find('\{', 0)

        while True:
            pos = view.find('\}', pos.end())
            if (pos.begin() == -1):
                break
            lastPos = pos.begin()

        return lastPos