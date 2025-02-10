---
title: "putty + tmux多窗口可用配置"
date: 2018-08-28T10:20:00
categories:
  - "Terminal"
tags:
  - "tmux"
  - "putty"
  - "ssh"
  - "windows"
draft: false
---
- putty的执行命令填入如下命令，tmux名称同session名称，以便开多个putty窗口时候识别

        $ tmux new -A -s {session_name}

- 添加.tmux.conf配置

        echo "
        ##########################################
        # STATUS BAR
        set -g status-keys vi
        set -g status-interval 1
        set -g status-attr bright
        set -g status-fg white
        set -g status-bg black
        set -g status-left-length 20
        set -g status-left '#[fg=green][#[fg=red]#S#[fg=green]]#[default]'
        set -g status-justify centre
        set -g status-right '#[fg=green][ %m/%d %H:%M:%S ]#[default]'
        setw -g window-status-current-format '#[fg=yellow](#I.#P#F#W)#[default]'
        setw -g window-status-format '#I#F#W'


        ##########################################
        # TERMINAL EMULATOR TITLES
        set -g set-titles on
        set -g set-titles-string \"#(tmux ls | awk -F: '{print $1}' | xargs | sed 's/\ / | /g')\"

        # Scroll History
        set -g history-limit 30000

        # Set ability to capture on start and restore on exit window data when running an application
        setw -g alternate-screen on

        # Lower escape timing from 500ms to 50ms for quicker response to scroll-buffer access.
        set -s escape-time 50
        " > .tmux.conf

- （可选）Shell标题控制， 在.profile文件里添加

        look_for_cmd=0
        print_cmd() {
          if [ ${look_for_cmd} = 1 ] ;then
            if [ "${BASH_COMMAND}" != 'print_host' ] ;then
              cmdline=$(history 1 | xargs | cut -d\  -f3-)
              if [[ "${cmdline}" =~ ^(sudo|ssh|vi|man|more|less)\  ]] ;then
                first=$(echo "${cmdline}" | awk '{print $1}')
                for i in ${cmdline} ;do
                  if ! [[ "${i}" =~ ^-.*$ ]] && ! [[ "${i}" =~ ^${first}$ ]] ;then
                    cmd="${first}[${i}]"
                    break
                  fi
                done
              elif [[ "${cmdline}" =~ ^[A-Z]*=.*$ ]] ;then
                cmd=$(echo ${cmdline} | awk '{print $2}')
              else
                cmd=$(echo ${cmdline} | awk '{print $1}')
              fi
              echo -ne "\033k${cmd}\033\\" 1>&2
              look_for_cmd=0
            else
              return
            fi
          fi
        }

        print_host() {
          echo -ne "\033k${HOSTNAME}\033\\" 1>&2
          look_for_cmd=1
        }

        PROMPT_COMMAND="print_host"

        trap "print_cmd" DEBUG