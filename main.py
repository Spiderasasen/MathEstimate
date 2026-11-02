#consents

#for claude
EXCHANGES_PER_MINUTE = 1   # typical; use 2 for fast chatting
INTRO_OUTRO = 2

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
def grokMath(x: int, s: int = 300, w: int = 20, u: int = 40, c: int = 100) -> float:
    """Cost in USD of one round with x wrong attempts (Grok 4.7 pricing)."""
    if x < 0:
        raise ValueError("x can't be negative")

    total_input = 2 * s + (x + 1) * (s + w + u)
    total_output = 2 * w + (x + 1) * c

    return round(total_input * 0.000002 + total_output * 0.000006, 6)

#main function of seeing which ai math equation are we going to use
def which_model(model: str) -> float | None:
    try:
        students = int(input("How many students?\n"))
        if students < 1:
            raise ValueError("Need at least 1 student")

        if model == "c":
            minutes = float(input("How many minutes of conversation each?\n"))
            if minutes <= 0:
                raise ValueError("Minutes must be positive")

            amount_of_messages = round(minutes * EXCHANGES_PER_MINUTE) + INTRO_OUTRO
            print(f"Estimated API calls per student (including intro and outro): {amount_of_messages}")
            per_student = claudeMath(amount_of_messages)

        elif model == "g":
            x = int(input("How many wrong attempts per round?\n"))
            if x < 0:
                raise ValueError("Wrong attempts can't be negative")

            rounds = int(input("How many rounds per student?\n"))
            if rounds < 1:
                raise ValueError("Need at least 1 round")

            print(f"Estimated API calls per student: {(x + 3) * rounds}")
            per_student = grokMath(x) * rounds

        else:
            return None

        print(f"Per student: ${per_student:.4f}")
        return per_student * students

    except ValueError as e:
        print(f"Invalid input: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

#main function
def main():
    while True:
        try:
            choice: int = int(input("Please chose an ai model\n 1.Claude\n 2.Grok\n 3.Exit\n"))
            match choice:
                case 1:
                    print("Claude")
                    total = which_model("c")
                    if total is not None:
                        print(f"Total estimated cost: ${total:.4f}")
                case 2:
                    print("Grok")
                    total = which_model("g")
                    if total is not None:
                        print(f"Total estimated cost: ${total:.4f}")
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