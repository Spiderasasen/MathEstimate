# claude code
def claudeMath(n: int, worst_case: bool = False) -> float:
    """Total cost in USD of a chat with n messages (Opus 5.5 pricing)."""
    if n < 1:
        raise ValueError("n must be at least 1")

    S: int = 500    # system prompt tokens
    U: int = 50     # avg user message tokens
    R: int = 1000 if worst_case else 150   # reply tokens (1000 = max_tokens ceiling)

    total_input = n * (S + U) + (U + R) * n * (n - 1) // 2
    total_output = n * R

    return round(total_input * 0.000004 + total_output * 0.00002, 4)


#grok

#main function of seeing which ai math equation are we going to use
def which_model(model: str) -> float | None:
    try:
        amount_of_messages: int = int(input("How many minutes of conversation are you thinking to have?\n"))
        amount_of_messages *= 2
        print(f"amount of messages per minute: {amount_of_messages}")
        amount_of_messages += 2
        print(f"amount of messages including the intro and outro messages: {amount_of_messages}")

        if model == "c":
            return claudeMath(amount_of_messages)
        elif model == "g":
            return 0.1

    except ValueError:
        print("Invalid amount of messages sent.")
        return None
    except Exception as e:
        print(f"Error: {e}")


#main function
def main():
    while True:
        try:
            choice: int = int(input("Please chose an ai model\n 1.Claude\n 2.Grok\n 3.Exit\n"))
            match choice:
                case 1:
                    print("Claude")
                    print(which_model("c"))
                case 2:
                    print("Grok")
                    print(which_model("g"))
                case 3:
                    break
                case _:
                    raise ValueError("Invalid choice")
        except ValueError:
            print("Invalid choice")
            continue
        except Exception as e:
            print(f"Error occurred, {e}")
            break

if "__main__" == __name__:
    main()