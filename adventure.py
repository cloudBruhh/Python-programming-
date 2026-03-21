
easter_egg_activator = False
easter_egg_count = 0


def slow_print(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
    print()


def check_easter_egg(response):
    global easter_egg_activator, easter_egg_count
    easter_eggs = ["banana", "42", "xyzzy", "plugh"]
    if response.lower().strip() in easter_eggs:
        easter_egg_count += 1
        if easter_egg_count >= 3:
            easter_egg_activator = True
            slow_print("\n*** Something strange happens... ***")
            return True
    return False


def get_choice(options):
    for i, option in enumerate(options, 1):
        print(f"  [{i}] {option}")
    while True:
        choice = input("\n> ").strip()
        if choice.lower() == "quit":
            print("\nThanks for playing!")
            exit()
        if check_easter_egg(choice):
            print("\n*** You found a secret! ***")
        try:
            idx = int(choice)
            if 1 <= idx <= len(options):
                return idx
        except ValueError:
            pass
        print("Invalid choice. Enter a number.")


def intro():
    slow_print("\n" + "=" * 50)
    slow_print("        THE MYSTERIOUS FOREST")
    slow_print("=" * 50)
    slow_print("\nYou wake up in a dark forest. The trees are tall,")
    slow_print("ancient, and covered in glowing moss. A faint path")
    slow_print("lies ahead, but you also notice a glimmering cave")
    slow_print("to your left and strange footprints leading into")
    slow_print("the brush.")
    slow_print("\nWhat do you do?\n")
    choice = get_choice(
        [
            "Follow the path",
            "Enter the cave",
            "Investigate the footprints",
            "Look for another way",
        ]
    )
    return choice


def path_scene():
    slow_print("\nYou walk down the winding path. The moss glows")
    slow_print("brighter as you progress. Soon, you reach a fork:")
    slow_print("one path leads to a cottage with smoke rising from")
    slow_print("the chimney, the other to a riverbank.\n")
    choice = get_choice(["Go to the cottage", "Head to the riverbank", "Go back"])
    return choice


def cave_scene():
    slow_print("\nThe cave entrance is cold and damp. Deep inside,")
    slow_print("you see two tunnels: one glitters with crystals,")
    slow_print("the other echoes with a low humming sound.\n")
    choice = get_choice(
        ["Follow the crystal tunnel", "Follow the humming tunnel", "Go back"]
    )
    return choice


def footprints_scene():
    slow_print("\nYou push through the brush and find a small")
    slow_print("clearing. A fluffy creature with eight eyes")
    slow_print("stares at you. It seems curious, not aggressive.\n")
    choice = get_choice(
        [
            "Approach the creature",
            "Back away slowly",
            "Offer it something from your pockets",
        ]
    )
    return choice


def cottage_scene(ending=False):
    if ending:
        return
    slow_print("\nYou approach the cottage. An old woman opens the")
    slow_print("door and smiles warmly.")
    if easter_egg_activator:
        slow_print("She winks and says, 'Ah, the one who knows the")
        slow_print("old words! Come in, come in!'")
    else:
        slow_print("'Lost, are you? Come inside, I have tea.'")
    slow_print("\nShe offers you a cup. Inside, you notice a map on")
    slow_print("the wall showing the way out of the forest.\n")
    choice = get_choice(
        [
            "Drink the tea and study the map",
            "Politely decline and leave",
            "Ask about the glowing moss",
        ]
    )
    return choice


def riverbank_scene():
    slow_print("\nThe riverbank is peaceful. A small boat rests on")
    slow_print("the shore, and downstream you see a waterfall with")
    slow_print("something sparkling behind it.\n")
    choice = get_choice(
        [
            "Take the boat downstream",
            "Investigate the waterfall",
            "Sit by the river and rest",
        ]
    )
    return choice


def crystal_tunnel_scene():
    slow_print("\nThe crystals grow brighter. You reach a chamber")
    slow_print("filled with gemstones. In the center, a pedestal")
    slow_print("holds a glowing orb.\n")
    choice = get_choice(
        ["Take the orb", "Examine the chamber carefully", "Leave it alone"]
    )
    return choice


def humming_tunnel_scene():
    slow_print("\nThe humming grows louder. You enter a vast")
    slow_print("underground lake with a small island in the")
    slow_print("center. On the island sits a sleeping giant.\n")
    choice = get_choice(
        [
            "Try to row to the island",
            "Quietly explore the shore",
            "Call out to the giant",
        ]
    )
    return choice


def creature_friendly_scene():
    slow_print("\nThe creature nuzzles your hand. A tiny key falls")
    slow_print("from around its neck. You pick it up.\n")
    choice = get_choice(["Use the key somewhere", "Keep it and explore"])
    return choice


def secret_ending():
    slow_print("\n" + "=" * 50)
    slow_print("   *** SECRET ENDING: THE CHOSEN ONE ***")
    slow_print("=" * 50)
    slow_print("\nThe easter egg words have resonated through the")
    slow_print("forest. The ancient trees bow as you pass.")
    slow_print("You discover you are the legendary Forest Walker,")
    slow_print("destined to protect this realm forever.")
    slow_print("\nCONGRATULATIONS! You found the secret ending!\n")
    play_again()


def normal_ending(msg):
    slow_print("\n" + "=" * 50)
    slow_print("             THE END")
    slow_print("=" * 50)
    slow_print(f"\n{msg}\n")
    play_again()


def play_again():
    print("\nPlay again? (yes/no)")
    if input("> ").strip().lower().startswith("y"):
        global easter_egg_count, easter_egg_activator
        easter_egg_count = 0
        easter_egg_activator = False
        main()
    else:
        print("\nThanks for playing! Goodbye.")
        exit()


def main():
    state = intro()

    if state == 1:
        state = path_scene()
        if state == 1:
            cottage_scene()
            choice = get_choice(["Trust her completely", "Keep your guard up"])
            if choice == 1:
                normal_ending(
                    "The wise woman becomes your mentor. You learn the secrets of the forest and live happily among its wonders."
                )
            else:
                normal_ending(
                    "Your caution serves you well. You find your own way home, wiser and stronger."
                )
        elif state == 2:
            state = riverbank_scene()
            if state == 1:
                normal_ending(
                    "The boat carries you downstream. You emerge from the forest, forever changed by the journey."
                )
            elif state == 2:
                if easter_egg_activator:
                    secret_ending()
                else:
                    normal_ending(
                        "Behind the waterfall, you find a treasure chest. Inside is a compass that always points to home."
                    )
            else:
                normal_ending(
                    "Resting by the river, you meet a friendly fish who offers to guide you out of the forest."
                )
        else:
            main()
    elif state == 2:
        state = cave_scene()
        if state == 1:
            state = crystal_tunnel_scene()
            if state == 1:
                normal_ending(
                    "The orb grants you the power of foresight. You become the forest's seer, guiding lost travelers."
                )
            elif state == 2:
                normal_ending(
                    "You discover ancient inscriptions. Deciphering them reveals a hidden exit from the forest."
                )
            else:
                normal_ending(
                    "Wisdom! The orb was a trap. By leaving it alone, you avoid a curse and find a safe path home."
                )
        elif state == 2:
            state = humming_tunnel_scene()
            if state == 1:
                normal_ending(
                    "The giant wakes and, mistaking you for a mouse, gently relocates you to the forest's edge. You laugh all the way home."
                )
            elif state == 2:
                normal_ending(
                    "You find a boat and row silently. On the island, you discover ancient wisdom and become the forest's keeper."
                )
            else:
                normal_ending(
                    "The giant awakens! But it's friendly and asks for help with a crossword puzzle. In thanks, it shows you the way home."
                )
        else:
            main()
    elif state == 3:
        state = footprints_scene()
        if state == 1:
            creature_friendly_scene()
        elif state == 2:
            normal_ending(
                "The creature blinks out of existence. Was it real? You shake it off and eventually find your way home."
            )
        else:
            normal_ending(
                "You find a snack in your pocket. The creature loves it and leads you to a magical portal home."
            )
    else:
        slow_print("\nYou find a hidden trail and follow it.")
        normal_ending(
            "Your instinct was right. The trail leads directly out of the forest. Sometimes the longest way is the shortest way home."
        )


if __name__ == "__main__":
    main()
