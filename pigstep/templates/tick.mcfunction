#!tag "minecraft:tick"

#!set note_function = generate_path("note")

execute as @a[tag={{ song_play }}] at @s run function {{ note_function }}

#!function note_function
    #!for node in generate_song()
        #!function node.parent append
            #!if node.partition(8)
                execute if entity @s[scores={ {{ song_tick }} = {{ node.range }} }] run function {{ node.children }}
            #!else
                #!set notes = node.value[1]

                #!if notes | length == 1
                    execute if entity @s[scores={ {{ song_tick }} = {{ node.range }} }] run {{ notes[0].play(song_player, song_source) }}
                #!else
                    #!set chord_function = generate_path("chord/{hash}", notes)
                    execute if entity @s[scores={ {{ song_tick }} = {{ node.range }} }] run function {{ chord_function }}

                    #!function chord_function
                        #!for note in notes
                            {{ note.play(song_player, song_source) }}
                        #!endfor
                    #!endfunction
                #!endif
            #!endif
        #!endfunction
    #!endfor

    scoreboard players add @s {{ song_tick }} 1
#!endfunction
