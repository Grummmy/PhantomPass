# PhantomPass
## ℹ️ Overview

##### Forgot your password again? Tired of coming up with new passwords? Your weak password 20030917John is hacked again? - the solution is PhantomPass! With PhantomPass you can remember only one password, and it can be as weak as `1234`

PhantomPass - is a powerful password generator, creating unique and reproducible passwords, based on your login and salt. Passwords are not stored, but generated on the fly, making the approach both secure and convenient.

## 📦 Requirements
- Python 3.6+
- `pyperclip` module for using password copying feature

## 🚀 Fast Start
```shell
python main.py <login/email/data>
```
if salt(`--salt`) is not set, it will be requested by an invisible input(using `getpass`).

## 🔧 Arguments and flags
| Flag                        | What does?                                                                                             |
| --------------------------- | ------------------------------------------------------------------------------------------------------ |
| `login`                     | Required, email or login from which you want to create password                                        |
| `-s`, `--salt`              | Salt, used in password creation. If not set by flag, will be requested with password input             |
| `-l`, `--length`            | Password length (default `12`)                                                                         |
| `-i`, `--index`             | Start index for slicing the password from the base64 hash. Passwords usually are shorter than b64 hash |
| `-a`, `--algorithm`, `-alg` | Hash-algorithm (`sha1`, `sha256`, `sha512`). (default `sha512`)                                        |
| `-e`, `--encoding`          | String encoding (default `utf-8`)                                                                      |
| `-c`, `--copy`              | Copy password to clipboard, after password generation                                                  |
| `-p`, `--print`             | Print password to console, after password generation                                                   |
| `-iw`, `--ignore-warnings`  | Ignore password length check relative to hash (not recommended)                                        |

> ⚠️ if both --print and --copy are specified, script will choose --copy.

## 🔒 Customization (highly recommended)
By customizing the script you are increasing the uniqueness of your passwords, which increases their security. The more customized the script is, the more branching paths an attacker must follow - and every wrong turn leads them further from your password. Each line of code that changes outcome adds hundreds new paths for attacker to pick the right one from.

In the code I mentioned 3 `MODIFIABLE` functions, which are recommended to modify at least with several minor changes **before real script use**.
#### `get_data()`
defines how your data(login/mail) are combined with salt. You can append extra symbol or a separator symbol.
#### `get_pswd(b64str)`
defines how password is sliced from base64 hash. default function only slices `length` symbols from defined `index`, if there are not enough symbols you'll get the warning.
#### `enhance(pswd)`
modifies the final password. by default, changes first `a` to `@`. it's recommended to add custom logic of enhancing your password.

## 🛡️ Security
PhantomPass does not store passwords, it generates them in runtime from several components. If one of components is missing - you and no one else is able to recreate your password, only if they are so fortunate to guess it. Here are required elements to recreate your password:
- login(or any other data)
- salt
- correct algorithm
- correct index and length
- script structure

Which means:
- same input = same password
- forgot salt or settings = forgot password
- changing the script after use = passwords lost

> Since recreating your password requires all 5 components, you can safely store your salt anywhere you want - it’s useless on its own.

## ⚙️ How the Password is Generated (Default Logic)

By default, PhantomPass generates a password using this exact pipeline:

1. **User input**  
    You pass a login (or any string) via CLI, and optionally a `--salt`.
2. **Salt acquisition**
    - If `--salt` is passed, it’s used as-is.
    - Otherwise, you'll be prompted to input it (invisible input via `getpass`).
3. **Input combination (`get_data()`)**  
    The script combines your login and salt **into one string**:
    ```python
    data = login + salt
    ```
4. **Hashing**  
    This combined string is hashed with the selected algorithm (`sha512` by default):
    ```python
    hash_bytes = hashlib.new(args.algorithm, data.encode(encoding)).digest()
    ```
5. **Base64 Encoding**  
    The hash is converted to a base64 string (without padding):
    ```python
    b64str = base64.b64encode(hash_bytes).replace(b"=", b"").decode(encoding)
    ```
6. **Slicing the password (`get_pswd()`)**  
    A substring is taken from the base64 string starting at `--index` with length `--length`:
    ```python
    pswd = b64str[index : index + length]
    ```
7. **Enhancing the result (`enhance()`)**  
    The password string is slightly modified for extra randomness. By default, it replaces the **first** `'a'` with `'@'`:
    ```python
    pswd = pswd.replace("a", "@", 1)
    ```
8. **Output**
    - If `--copy` is set → password is copied to clipboard
    - If `--print` is set → password is printed
    - If neither is set → script will ask what to do
