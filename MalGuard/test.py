from guarddog import NPMPackageScanner
scanner = NPMPackageScanner()

str = """
rules:
  - id: npm-install-script
    message: The package.json has a script automatically running when the package is installed
    metadata:
      description: Identify when a package has a pre or post-install script automatically running commands
    patterns:
      - pattern-inside: |
          "scripts": {...}
      - pattern-either:
        - pattern: |
            "preinstall": $VAR
        - pattern: |
            "postinstall": $VAR
        - pattern: |
            "install": $VAR
      # note that on some cases installing a package can lead to the execution of some "prepare" scripts
      # (typically when a dependency is a git repository, see https://github.com/npm/cli/issues/6031#issuecomment-1449119423)
      # however this happens pretty rarely so reporting every package with a "prepare" script would be too noisy;
      # see https://github.com/DataDog/guarddog/issues/308
      - metavariable-pattern:
          metavariable: $VAR
          pattern-regex: ^(?!"(npx patch-package|nuxt prepare|npx only-allow pnpm|prisma generate|ibmtelemetry --config=telemetry.yml|husky install|tsc \|\| exit 0|patch-package|husky|echo \"preinstall script\")").*$
    languages:
      - json
    paths:
      include:
        - "*/package.json"
        - "*/npm-install-script.json" # unit test
    severity: WARNING

"""


result = scanner.scan_local('./dataset/npm/1ru-cache-0.0.1', rules={"id1","id2"})

print(result)