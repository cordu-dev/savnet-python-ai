def reciprocal(n, fake_assert_exception=False):
    try:
        if fake_assert_exception:
            assert 1 == 0

        n = 1 / n
    except ZeroDivisionError:
        print("Division failed")
        n = None
    else:
        print("Everything went fine")
    finally:
        print("It's time to say goodbye")
        return n


print(reciprocal(2))
print(reciprocal(0))
print(reciprocal(66, fake_assert_exception=True))
