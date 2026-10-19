# AI Use Note

AI assistants (ChatGPT) were used to help reconstruct and debug parts of the educational QKD code, write tests, interpret plots, and draft documentation. The project author is responsible for reviewing and understanding all code and results.

**Specific error and verification:** An AI-generated `requirements.txt` initially contained literal `\n` text instead of separate package lines. Running `python -m pip install -r requirements.txt` produced an “Invalid requirement” error, which exposed the formatting problem. The file was corrected to one requirement per line, and the project test suite was then run successfully (12 tests passed in the author's Windows/Python 3.12.4 environment).

The results were also checked against the analytic reference trends `QBER = f/4` for the idealized intercept-and-resend attack and `QBER ≈ 2p/3` for the simplified random Pauli-error model. These checks support the expected behavior of this simulation; they do not establish security of a real QKD system.
