# Changelog

## [0.8.2](https://github.com/liblaf/ai-commit-cli/compare/v0.8.1...v0.8.2) (2024-06-15)

### 🐛 Bug Fixes

- update release-please config and refactor CLI imports ([4d0d878](https://github.com/liblaf/ai-commit-cli/commit/4d0d878ff70cb6e4f3bb76595df3ed01d711d316))

## [0.8.1](https://github.com/liblaf/ai-commit-cli/compare/v0.8.0...v0.8.1) (2024-06-09)

### 🐛 Bug Fixes

- **api:** update model not found error message ([15becbb](https://github.com/liblaf/ai-commit-cli/commit/15becbb76516d1d77ec8f8fe5defbab7b92e73c0))
- update optional type annotations for pathspec, api_key, and base_url ([ff63961](https://github.com/liblaf/ai-commit-cli/commit/ff639617e133e6a0b2427e3c2220fcf70babada8))

### 🏗 Miscellaneous Chores

- **deps:** update python docker tag to v3.12.4 ([a29e127](https://github.com/liblaf/ai-commit-cli/commit/a29e12727a6d627415d77780ea22ff0b90c4dda3))

### 💻 Continuous Integration

- **repo:** sync with repo template ([730d778](https://github.com/liblaf/ai-commit-cli/commit/730d778c94009e0b8242ade78fbf600a39bf8e92))
- **repo:** sync with repo template ([62141f9](https://github.com/liblaf/ai-commit-cli/commit/62141f999ff04a6a7625dcbda2be1ea9b6f774d8))
- **repo:** sync with repo template ([743c1c6](https://github.com/liblaf/ai-commit-cli/commit/743c1c675fd239ee1ae4bf75f0af4b6dd672e3a4))
- **repo:** sync with repo template ([c92d3fb](https://github.com/liblaf/ai-commit-cli/commit/c92d3fb1594be167e752942016b57922ff798051))

## [0.8.0](https://github.com/liblaf/ai-commit-cli/compare/v0.7.0...v0.8.0) (2024-05-11)

### ✨ Features

- add a template for generating conventional commit messages based on code diffs, types, scopes, and breaking changes. ([af2b654](https://github.com/liblaf/ai-commit-cli/commit/af2b6548789893e7d08077bdd5a63816f91bf181))
- **ci:** improve build process by activating virtual environment ([afdd378](https://github.com/liblaf/ai-commit-cli/commit/afdd3787f83c8d9b076ec2aa4c86e2809a1b9477))
- update script configuration for 'aic' command ([2dd2037](https://github.com/liblaf/ai-commit-cli/commit/2dd20373bacb40961c8d1e7412db64255f308954))

### 🐛 Bug Fixes

- **ai_commit_cli/prompt:** update prompt message for determining scope ([142871d](https://github.com/liblaf/ai-commit-cli/commit/142871d44d66ceae2c07f1697dcd6bb4e6610020))
- **cli:** sanitize response messages to remove unnecessary content ([9423949](https://github.com/liblaf/ai-commit-cli/commit/9423949c9cf193ba4e2bab985e90d30761e18e17))
- **deps:** update dependency httpx to v0.27.0 ([11f9096](https://github.com/liblaf/ai-commit-cli/commit/11f90966a6593ca7d99f3f5cbcd15a3aa6019f49))
- **deps:** update dependency openai to v1.13.3 ([18921a7](https://github.com/liblaf/ai-commit-cli/commit/18921a70dbc418ec75790672377d1c9993708333))
- **deps:** update dependency rich to v13.7.1 ([db8833b](https://github.com/liblaf/ai-commit-cli/commit/db8833b858229380d0ff241b4c6d47f12c97dec6))
- enhance displaying type of change ([4273518](https://github.com/liblaf/ai-commit-cli/commit/4273518cf94e3fc2a5081f4192f666c5768d3300))
- **provider/openai:** correct token truncation calculation ([a1a69eb](https://github.com/liblaf/ai-commit-cli/commit/a1a69ebb23e984fd185c7d287782e48bb0d6fc01))
- sanitize message by stripping leading and trailing whitespace ([885e95d](https://github.com/liblaf/ai-commit-cli/commit/885e95df3d435fd3df1d46d3f2f315ffe0fd5139))
- update git commit function signature to include keyword arguments ([9e80833](https://github.com/liblaf/ai-commit-cli/commit/9e80833258b8c6e1622df83787f24ba4ca306070))
- update pathspec to include all lock files ([6aaf2c2](https://github.com/liblaf/ai-commit-cli/commit/6aaf2c2bfdb85656fd0394eeccc706342f101be1))
- update script configuration in pyproject.toml ([df68792](https://github.com/liblaf/ai-commit-cli/commit/df687927c24529c89a5156f3fe9d0d43e316c6fa))

### 📚 Documentation

- add reference to experimental metaprompt feature ([7226896](https://github.com/liblaf/ai-commit-cli/commit/7226896be992cbf3be3d54c4fd879181bcb5654d))

### 🎨 Styles

- refactor code formatting in Makefile and add ruff.toml for linting configuration. ([86ed400](https://github.com/liblaf/ai-commit-cli/commit/86ed4005c5dd0fbd4db886e77704dc93a976ce64))
- update method signatures for consistency with async/await syntax ([09a8936](https://github.com/liblaf/ai-commit-cli/commit/09a89367528909e883ace2ecd73aa3db0c9d5c4f))

### 🏗 Miscellaneous Chores

- **deps:** update dependency httpcore to v1.0.4 ([7952ecc](https://github.com/liblaf/ai-commit-cli/commit/7952ecc782d84bd3d629daed20775fbc6a120196))
- **deps:** update dependency nuitka to v2.0.4 ([5bd5316](https://github.com/liblaf/ai-commit-cli/commit/5bd5316e05da406b717558eb64f8c8393f14fd55))
- **deps:** update dependency nuitka to v2.0.5 ([59de0bf](https://github.com/liblaf/ai-commit-cli/commit/59de0bfd49f586756108eefc279b5d7efb6678b9))
- **deps:** update dependency nuitka to v2.0.6 ([06f7323](https://github.com/liblaf/ai-commit-cli/commit/06f7323a383c6aa0e8e02ea7b1eb517795bf7616))
- **deps:** update dependency nuitka to v2.1 ([1caff43](https://github.com/liblaf/ai-commit-cli/commit/1caff43c228938ba35c543066164ee7b28650331))
- **deps:** update dependency nuitka to v2.1.1 ([3c2e67b](https://github.com/liblaf/ai-commit-cli/commit/3c2e67bd28a9a88fb4eccd0a5a83c095304ad3d2))
- **deps:** update dependency openai to v1.13.3 ([d0d1aed](https://github.com/liblaf/ai-commit-cli/commit/d0d1aed0fa389aaafc21d055c0c0353577d9f1b6))
- **deps:** update dependency pydantic-core to v2.16.3 ([9122da0](https://github.com/liblaf/ai-commit-cli/commit/9122da099ca8a6facdb32b87b8c53d19f777abfb))
- **deps:** update dependency pyinstaller to v6.5.0 ([f7a4c76](https://github.com/liblaf/ai-commit-cli/commit/f7a4c7676f684a8a8825811410fed8ab6611c719))
- **deps:** update dependency rich to v13.7.1 ([f84f8f6](https://github.com/liblaf/ai-commit-cli/commit/f84f8f633dfd2f5d6c0f5b6f1fd9af1699de6733))
- **deps:** update dependency sniffio to v1.3.1 ([d2fa363](https://github.com/liblaf/ai-commit-cli/commit/d2fa3630c838cbf0f37ff3e2d54b141209a4b0d1))
- **deps:** update dependency typing-extensions to v4.10.0 ([409a100](https://github.com/liblaf/ai-commit-cli/commit/409a100ee62c058d7036f013d24a27fce175a84a))
- **deps:** update eifinger/setup-rye action to v3 ([055e9a0](https://github.com/liblaf/ai-commit-cli/commit/055e9a0bdebeeccde02ab994dbb6d72524bcb5fe))
- **deps:** update python docker tag to v3.12.2 ([7b0169d](https://github.com/liblaf/ai-commit-cli/commit/7b0169dfbf9eaf89998f85de1836017a115b5caa))
- **deps:** update python docker tag to v3.12.3 ([1de60a0](https://github.com/liblaf/ai-commit-cli/commit/1de60a0b2f0802116d08bece732dae88577245c5))

### 📦 Build System

- **deps-dev:** Bump the pip group with 2 updates ([#48](https://github.com/liblaf/ai-commit-cli/issues/48)) ([f7c2878](https://github.com/liblaf/ai-commit-cli/commit/f7c2878c260fb64a11103078bc6c635d336b31f2))
- **deps:** Bump openai from 1.11.0 to 1.11.1 ([#45](https://github.com/liblaf/ai-commit-cli/issues/45)) ([36ef730](https://github.com/liblaf/ai-commit-cli/commit/36ef730818729d5c11cd6c8d8b00f267167c951e))
- **deps:** Bump the pip group with 2 updates ([#47](https://github.com/liblaf/ai-commit-cli/issues/47)) ([36ab2da](https://github.com/liblaf/ai-commit-cli/commit/36ab2da7d20e06cac4ce7a48e128b139491eb637))
- **deps:** update pydantic and typing-extensions versions ([975db37](https://github.com/liblaf/ai-commit-cli/commit/975db37c15306f8c1eb53245b46739c46cc97103))

### 💻 Continuous Integration

- **.github/workflows/ci.yaml:** update CI workflow to install necessary tools ([8df5a7a](https://github.com/liblaf/ai-commit-cli/commit/8df5a7af65579787a40b59f0ebe4ef5af7c39218))
- configure Release Please workflow for automated versioning and changelog generation ([c494eae](https://github.com/liblaf/ai-commit-cli/commit/c494eae3e8b0e953a9c4c2e758a3ba8bcc79af3b))
- **pre-commit:** auto fixes from pre-commit hooks ([b2d2bd7](https://github.com/liblaf/ai-commit-cli/commit/b2d2bd76c7d078068b5b7b5d95ea88ce3e390717))
- **pre-commit:** auto fixes from pre-commit hooks ([6c64ebb](https://github.com/liblaf/ai-commit-cli/commit/6c64ebb8698a44c8581542ce7fe90614f51d6baa))
- **pre-commit:** pre-commit autoupdate ([#46](https://github.com/liblaf/ai-commit-cli/issues/46)) ([895d841](https://github.com/liblaf/ai-commit-cli/commit/895d84193bb6b86b47238c408718b31d38675285))
- **pre-commit:** pre-commit autoupdate ([#49](https://github.com/liblaf/ai-commit-cli/issues/49)) ([124b2d5](https://github.com/liblaf/ai-commit-cli/commit/124b2d556f452bc46c742dfd570c43a3674e330b))
- **repo:** sync with repo template ([f2d0148](https://github.com/liblaf/ai-commit-cli/commit/f2d01488183f639c5d81483d867cb59abf9083db))
- **repo:** sync with repo template ([baca37b](https://github.com/liblaf/ai-commit-cli/commit/baca37b4f3271a2535f6eb45b9841154c727f26a))
- **repo:** sync with repo template ([dfab5f0](https://github.com/liblaf/ai-commit-cli/commit/dfab5f00f1e104cb670e3bdc5b048e907141d508))
- **repo:** sync with repo template ([7c14a66](https://github.com/liblaf/ai-commit-cli/commit/7c14a66eeeab1acbe9557ee9268565c34772a0ec))
- **repo:** sync with repo template ([fc38dfe](https://github.com/liblaf/ai-commit-cli/commit/fc38dfe6b451f70eaf022e2b9f078c2ab6a92c05))
- **repo:** sync with repo template ([6c694da](https://github.com/liblaf/ai-commit-cli/commit/6c694daea625977a3b7e52da6b9c8be72b974a44))
- **repo:** sync with repo template ([989615d](https://github.com/liblaf/ai-commit-cli/commit/989615d7b34c8b48ea360a687aca8d98d2838639))
- **repo:** sync with repo template ([c53ae08](https://github.com/liblaf/ai-commit-cli/commit/c53ae0839d56ff2476c96f84734799494ba58205))
- **repo:** sync with repo template ([aeda647](https://github.com/liblaf/ai-commit-cli/commit/aeda6473dabd9b206b94b16a4fa5993ed1f469f3))
- **repo:** sync with repo template ([c1be455](https://github.com/liblaf/ai-commit-cli/commit/c1be455ffa7e53ee1a472c4810ba1a0ed5d12c3a))
- **repo:** sync with repo template ([890a265](https://github.com/liblaf/ai-commit-cli/commit/890a26511a5280c7f08f3acc16ed783e4352d907))
- **repo:** sync with repo template ([e7fba82](https://github.com/liblaf/ai-commit-cli/commit/e7fba82444c845b488b61ae8ffabce222a342825))
- **repo:** sync with repo template ([0ca3453](https://github.com/liblaf/ai-commit-cli/commit/0ca345335381bbd576b8e64a3fd0473546787295))
- sync with repository template ([fba62da](https://github.com/liblaf/ai-commit-cli/commit/fba62da717c2e1bdba5fc04c26ca33253b1cade4))
- sync with repository template ([5069008](https://github.com/liblaf/ai-commit-cli/commit/506900873ff09782f384057ef5fee528effa3927))
- sync with repository template ([6ba0f20](https://github.com/liblaf/ai-commit-cli/commit/6ba0f20e29af5f4c7f96845c794b48a454d55c39))
- sync with repository template ([a786370](https://github.com/liblaf/ai-commit-cli/commit/a7863704152113b1bc8865eda6a4d0aa5c47cfce))
- sync with repository template ([0f2c919](https://github.com/liblaf/ai-commit-cli/commit/0f2c9190608ea57408729eccb7dfbc7975031f25))
- sync with repository template ([7e15331](https://github.com/liblaf/ai-commit-cli/commit/7e15331f6c67d3f4b2181c7e252b8ec7278b626a))
- sync with template repository ([b815207](https://github.com/liblaf/ai-commit-cli/commit/b815207c056832b9a19fa42633225d7236a48803))
- sync with template repository ([83ad2df](https://github.com/liblaf/ai-commit-cli/commit/83ad2dfaa07dbe889e7aefeb13f79372f57d316b))
- sync with template repository ([d22947e](https://github.com/liblaf/ai-commit-cli/commit/d22947e3437a36fc28fb7b126c92344fe2cc505d))
- sync with template repository ([809cb97](https://github.com/liblaf/ai-commit-cli/commit/809cb97a95250fecae7d495b1d763a8bbd91a5e4))
- sync with template repository ([c550254](https://github.com/liblaf/ai-commit-cli/commit/c5502542e9cf1bbb62ee9b02d8b8111c367384b2))
- sync with template repository ([23c121a](https://github.com/liblaf/ai-commit-cli/commit/23c121ad6b87d7177f74ba6dac6715d31b6a9b4b))
- sync with template repository ([d5cdc80](https://github.com/liblaf/ai-commit-cli/commit/d5cdc80aa9009bdd571a3f233498264076b17e34))
- sync with template repository ([5474533](https://github.com/liblaf/ai-commit-cli/commit/5474533789e280a417c57d918b87c07dbe454d4c))
- sync with template repository ([150791d](https://github.com/liblaf/ai-commit-cli/commit/150791d863c64a88d66a3a0541873ffc18d2eba4))
- sync with template repository ([623a276](https://github.com/liblaf/ai-commit-cli/commit/623a27636ed7579791d71ddfd52d84fdf3afe61b))
- sync with template repository ([03ffbe7](https://github.com/liblaf/ai-commit-cli/commit/03ffbe75eafe5d8edaf412c833315eca38fc1b4a))
- sync with template repository ([caf2dda](https://github.com/liblaf/ai-commit-cli/commit/caf2dda6786271292a907d811fcf3e038d1228c7))
- sync with template repository ([4a9c150](https://github.com/liblaf/ai-commit-cli/commit/4a9c15086bebc5e0ff88518fa2e1eda62f01527a))
- **workflows:** add coreutils installation for brew and choco ([ea83810](https://github.com/liblaf/ai-commit-cli/commit/ea838106f17c910203c01cf6e17e63165d7cfc29))
- **workflows:** update CI workflows to use Taskfile for building packages ([839da7e](https://github.com/liblaf/ai-commit-cli/commit/839da7ebca2acb7ab61f49a75c03f1c2cbb03729))
