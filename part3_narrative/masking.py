def alias_for(reseller_id: str) -> str:
    number = reseller_id.replace("RS", "")
    
    if number == "019":
        return "ALIAS-19"
    elif number == "006":
        return "ALIAS-06"
    
    return f"ALIAS-{int(number):02d}"


def assert_no_raw_names_leak(text: str, names: list[str]) -> bool:
    return all(name not in text for name in names)


if __name__ == "__main__":
    # Positive test: raw reseller name is not present
    safe_text = "Top reseller ALIAS-19 generated the highest spend."
    names = ["Mumbai Reseller 1", "Ahmedabad Reseller 6"]

    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"
    assert assert_no_raw_names_leak(safe_text, names) is True

    # Negative test: raw reseller name is present
    unsafe_text = "Mumbai Reseller 1 generated the highest spend."
    assert assert_no_raw_names_leak(unsafe_text, names) is False

    print("Masking tests passed.")