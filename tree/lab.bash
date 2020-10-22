#!/bin/bash

if false
then
printf "\u2502\n" # │
printf "\u251c\n" # ├
printf "\u2500\n" # ─
printf "\u2514\n" # └
printf "\u00A0\n" # non-breaking space
printf "\u0020" # space
printf "\n\u2502\u00A0\u00A0\u0020\u2514\u2500\u2500\u0020 two\n"
fi


files_count=0
dirs_count=0
search() {
  subdirs=("$1"/*)
  local parent="$2"
  for each in "${subdirs[@]}"
  do
    name=$(basename ${each})
    if [ -f "${each}" ]
    then files_count=$((files_count+1));child="\u251c\u2500\u2500"; printf "${parent}${child}${name}\n"
    elif [ -d "${each}" ]
    then
      dirs_count=$((dirs_count+1));
      if [ -n "$(ls -A ${each})" ];
      then  child="\u2514\u2500\u2500\u2500"; printf "${parent}${child}${name}\n";
      search ${each} "${parent}\u2502\u0020\u0020\u0020\u0020"
      else
       child="\u251c\u2500\u2500"; printf "${parent}${child} ${name}\n";
      fi
    fi
  done
}

search "$1"
printf "${dirs_count} directories, ${files_count} files\n"


