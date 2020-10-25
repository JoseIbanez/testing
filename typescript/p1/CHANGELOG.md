## v1.7.1 - 10 Oct 2019

* Ensure .d.ts parts of src/ folder are visited by underlying tsc program as well.

## v1.7.0 - 09 Oct 2019

* Fix Promise.await ignored for async class-based method declarations
* Add support for module import
* Fix reference tracking for variable re-exporting with rename
* typescript 3.6.3 updated with support for EmitHelpers and __spreadArray by default.
* rework ESShim.merge implementation and fallback on default __asign EmitHelper provided by tsc.
* Update archetype tsConfig to limit runtime libs to only those supported by vRO
* remove custom implementation for .d.ts generation and fallback to tsc instetad to resolve numerous problems with declaration files
* fix number of issues with inaccessible properties being exported in transpiled code.
* reduce code optimizaiton efforts and ensure empty .d.ts & .js files are preserved as those might be referenced exernally.
* Fix support of empty files (e.g. pure-interfacees) on import/export transpiled code.
* Migrate to using tsc native class genration and super execution to support default decorators and reflect-metadata
* Fix source file traversal and transformation and thus simplifying literal/identifier/comments handling
* Remove custom super call handling and leave default tsc handling.
* Remove import optimizations as impacting correctness of imports.

## v1.6.0 - 11 Sep 2019

* vrealize:push goal now supports vCloud Director Angular UI extension projects
* Package installer now supports vCloud Director Angular UI extension projects
* Support for XML workflow representation in TypeScript projects
* Support for decorators in TypeScript projects.
* Implement support for vCloud Director Angular UI extension projects
* Support for vRO policies in TypeScript projects. Files ending with .pl.ts will be transpiled as a vRO policy template.
* Enhanced support for vRO resource elements in TypeScript projects.
* Enhanced support for vRO configurations and workflows in TypeScript projects.
* Windows support for TypeScript projects.

## v1.5.11 - 09 May 2019

### Enhancements
* Add ```generated.from``` Maven property to the root POM of all archetypes. This can be used to differentiate which "template" was used to generate the project, for example in the context of a CI pipeline.

## v1.5.10 - 19 Apr 2019

### Enhancements
* Include CHANGELOG.md in the final tool chain bundle.

## v1.5.9 - 19 Apr 2019

### Enhancements
* ```vro:pull```, ```vra:pull``` and ```vra:auth``` Maven goals now support the SSL verification flags to be set as properties in a Maven profile, similarly to the ```vrealize:push``` goal.

### Fixes
* When using the Bundle Installer with a properties file the value of ```vro_delete_old_versions``` used to be ignored - if the property was present, the installer would do the cleanup. Now, if the property is not present it is considered false. If it is present, however, its value will be used to opt-in for the cleanup.

## v1.5.8 - 15 Apr 2019

### Enhancements
* Support for gradual migration from JS-based projects to TypeScript ones by allowing .js files in src/ folder to be respected at TS copilation stage.
* Support for vRO resource elements to be included in package. TS projects can contain any files that are not .ts and .js under src/ directory and those will carried over.
* (internal) Improvement of unit-test parallel execution and sub-suite instantiation for easier debugging/testing purposes.

## v1.5.7 - 03 Apr 2019

### Enhancements
* Installer CLI now prompts for SSL verification flags. Default is still to verify the certificate against Java's key store (i.e. cacerts) and to verify the hostname. Those flags can be persisted and controlled via the environment's ```.properties``` file.
* vrealize:push Maven goal now supports the SSL verification flags to be set as properties in a Maven profile, i.e. you can add ```<vrealize.ssl.ignore.certificate>true</vrealize.ssl.ignore.certificate>``` under ```<properties>``` in an active Maven profile to skip the certificate verification against JAVA's key store (i.e. cacerts). You can also add ```<vrealize.ssl.ignore.hostname>true</vrealize.ssl.ignore.hostname>``` to skip the hostname verification. **WARNING** this is intended for use with production endpoints. For those cases, register vRA/vRO certificate in Java's key store and access the endpoint using its FQDN.

## v1.5.6 - 27 Mar 2019

### Enhancements
* __BREAKING__ All certificates are now verified as part of API calls from the toolchain to vRA/vRO:
  * Verify hostname - the hostname if the vRO/vRA server should match the CN of the SSL certificate. *For development environments, this can be skipped by a flag described in documentation.*
  * Verify certificate - the SSL certificate used by vRO/vRA is verified against the Java default keystore, i.e. ```cacerts```. Self-signed or third-party certificates have to either be addded to the trusted store (or their CA) or the check can be ignored for development environments by a flag described in documentation.

* Improved logging when installing packages - logs will report which package will be included (pass) and which will be excluded (skip).
* ```vrealize:push``` will import all packages per type in a single batch, reporting what will be included (pass) and excluded (skip).

### Fixes
* Installer overwrites newer versions of packages found on the server if a concrete source package, e.g. v1.0.2 is not found.
* ```vrealize:push``` downgrades dependent packages, i.e. it will always forcefully install the concrete versions of the dependencies regardless of the state of the target vRO/vRA server. This is still possible if an additianal flag is passed to the command: ```-Dvro.importOldVersions``` and respectively ```-Dvra.importOldVersions```.

## v1.5.5 - 14 Mar 2019

### Fixes
* Pulling a vRO actions project from a Windows workstation leads to wrong identation in actions JavaScript files.

## v1.5.4 - 13 Mar 2019

### Fixes
* Issue related to vRO multi-tenantcy authentication. When toolchain worked with a vRO in a multi-tenant mode it tooked tenant name as domain name instead of the real domain name for login which caused authentication issues for non-default tenants.
* Issue related to the unit-tests executor of vRO actions-based projects on Windows. Inability to run unit-tests on Windows development workstation.
* Regression issue related to import/export of vRA composite blueprints for vRA versions before 7.4, as custom forms API is not supported in these versions.

### Known Issues
* VS Code Extension and Maven plugins cannot work against default tenant (vsphere.local) and custom tenant at the same time, when vRO is configured in a multi-tenant mode. This limitations comes from multi-tenant implementation in vRO where Resource Elements created in the default tenant are read-only for all other tenants.
This issue could be worked around by not usting the toolchain against default tenant in multi-tenant environment.

## v1.5.3 - 05 Mar 2019

## v1.5.2 - 28 Feb 2019

## v1.5.1 - 11 Feb 2019

### Fixes
* Excessive collection triggering and 100 percent CPU usage for several minutes when VSCode auto-saving is enabled or frequent saves are used
    * Collection will be triggered only if files are created or deleted instead of on each change
    * Collection will be delayed with 10 seconds - that way when pulling many files the multiple change events will trigger only one colelction
* Run Action command now supports vRO 7.3 and lower
* Untitled files and files without IIFE now have correct autocompletion

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.
* Exporting vRA blueprints without custom forms logs error message "null". This is a bug in underling REST client library.

## v1.5.0 - 04 Feb 2019

### Enhancements
* New command in the vscode extension - **vRO: Run Action**
    * Allows running an action JavaScript file in vRO while seeing the logs in VSCode.
    * Available both in the Command Palette and as `zap` icon on the editor's tab bar.
* Implemented code coverage report produced by running Jasmin unit tests. The report is in lcov.info format, which is readable by Sonar.

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.
* Exporting vRA blueprints without custom forms logs error message "null". This is a bug in underling REST client library.

## v1.4.1 - 01 Feb 2019

### Enhancements
* New setting to *exclude* certain projects from the list of build tasks (`Cmd+Shift+B`) by using glob patterns
```javascript
"o11n.tasks.exclude" : [
    "com.vmware.pscoe.library*", // Exclude all PSCoE libraries
    "!com.vmware.pscoe.library*", // Exclude everything, except PSCoE libraries
    "com.vmware.pscoe.!(library*)", // Exclude everything PSCoE, except libraries
    "com.vmware.pscoe.library:{nsx,vra,vc}", // Exclude nsx, vra and vc libraries
    "com.vmware.pscoe.library:util" // Exclude util library (<groupId>:<artifactId>)
]
```

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.
* Exporting vRA blueprints without custom forms logs error message "null". This is a bug in underling REST client library.

## v1.4.0 - 25 Jan 2019

### Enhancements
* Support for [Multi-root Workspaces](https://code.visualstudio.com/docs/editor/multi-root-workspaces) that allow opening more than one vRO project into single vscode window.
* Dynamically create build tasks (`Cmd+Shift+B`) based on project's type and modules.
* New pom.xml diagnostics
    * Show inline warning, if toolchain version in pom.xml file is lower than the vscode extension's version.
    * Provide quick fix action in pom.xml that replaces the parent version with the vscode extension's version.
* Support for export/import of vRA custom forms.
* Support for clean up task of vRA/vRO packages from server.
    * Clean up of the current version and/or old versions and their dependencies.
    * Supported via "mvn" command or package installer

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.
* Exporting vRA blueprints without custom forms logs error message "null". This is a bug in underling REST client library.

## v1.3.10 - 01 Nov 2018

### Fixes
* The vscode extension cannot load when the project location contains spaces or other characters that are percent-encoded in URIs
* Push does not work for vRA packages built on Windows

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.

## v1.3.8 - 24 Oct 2018

### Fixes
* The vscode extension cannot generate projects with spaces in the workflows path parameter.

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.

## v1.3.7 - 19 Oct 2018

### Enhancements
* Autocomplete modules and actions in `Class.load()` statements
* Add a new task command (`vRO: Push Changes`) for pushing only the diff between current branch and origin/master
* Support specifying different command for windows in the vRO task definitions (.vscode/tasks.json)
* New Project wizard will reuse the current VSCode window if no other folder is opened.

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.

## v1.3.6 - 03 Oct 2018

### Fixes
* New project functionality works only from the context of existing IaC project. Now projects can be created from an empty VSCode window.

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.

## v1.3.5 - 25 Sep 2018

### Enhancements
* Include package installer in the toolchain to enable -Pbundle-with-installer. When a package is build with ```mvn package -Pbundle-with-installer``` this will produce a zip file with all the dependencies and a bin/ and repo/ folders. The bundle can be installed by unziping it and calling ./bin/installer.
* Archetype generated projects now work with release.sh immediately, i.e. without further modifying the pom.xml file of the root project. You can still have the SCM remote written in the POM and not specify it every time, but OOTB after you add the project to SCM and add your remote (origin) you can use the ```-r``` option of the **release.sh** script: ```sh ./release.sh -r $(git remote get-url origin)```

### Fixes
* vRealize archetype project's install workflow category path contains placeholders

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.
* New project functionality works only from the context of existing IaC project.

## v1.3.3 - 21 Sep 2018

### Fixes
* vRealize archetype produces a root pom with placeholders

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.
* New project functionality works only from the context of existing IaC project.

## v1.3.2 - 19 Sep 2018

### Fixes
* Actions with `-SNAPSHOT` in the version cannot be overridden in vRO version 7.3 or lower

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.

## v1.3.1 - 13 Sep 2018

### Fixes
* The New Project wizard shouldn't ask for Workflows Path when bootstrapping vRA YAML projects
* vRA YAML projects could not be created because of wrong archetype group ID

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.

## v1.3.0 - 11 Sep 2018

### Enhancements
* `vRO: New Project` command for bootstrapping vRA and vRO projects
* New maven archetype for vRA YAML projects
* Option to edit the profiles in maven's settings.xml file from the Pick Profile dialog (located at the bottom left corner of the status bar)
* Reduced the number of parameters needed for generating a project when using Maven archetype commands
    * **All types of projects**
        * Removed the parameters `-Dtop`, `-Dcompany`, `-Ddepartment`, `-Dtopic`, `-Dname`
        * Added the parameters `-DgroupId` and `-DartifactId`
    * **Projects containing workflows**
        * Removed the parameters `-DbaseCategory`, `-DsubCategory` and `-Dtitle`
        * Added the parameter `-DworkflowsPath`
* Jasmine tests no longer fail with cryptic error when there is an empty/invalid js action file

### Fixes
* `release.sh` cannot release vRA and mixed projects
* Package installer does not support special characters in the password field

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.

## v1.2.0 - 30 Jul 2018

### Enhancements
* All components in the toolchain are now capable of using vRA SSO as authentication mechanism towards vRO
* New options in the Maven profiles for vRO (located in user's settings.xml)
    * `<vro.auth>vra</vro.auth>` - use vRA SSO authentication
    * `<vro.auth>basic</vro.auth>` - use Basic authentication
    * `<vro.tenant>vsphere.local</vro.tenant>` - specify the tenant to be used for SSO authentication
* There is no longer separate vRO connection configuration for the toolchain Maven plugins and the VSCode extension. All components of the toolchain now use the connection settings defined in the Maven profile at `~/.m2/settings.xml`. The exact profile to be used by the VSCode extension is provided by a new setting `o11n.maven.profile`.
* More build and deploy tasks are available in the `Cmd+Shift+B` palette in VSCode. The actual command behind each of these tasks can be overwritten by a project local `.vscode/tasks.json` file (`Cmd+Shift+B` -> click the cogwheel icon for a task -> change the command in the generated tasks.json)

### Migration Steps
* Since v1.2.0, all mixed projects that have to use vRA SSO authentication, should have the following added to their root **pom.xml** file.
```xml
<parent>
    <groupId>com.vmware.pscoe.o11n</groupId>
    <artifactId>base-package</artifactId>
    <version>1.2.0</version>
</parent>
```
* `o11n.maven.profile` setting is now required by the VSCode extension

### Fixes
* Print a warning when `push` is executed for unsupported artifact types, instead of throwing an exception
* Fix the 'Extension 'vmw-pscoe.o11n-vscode-extension' uses a document selector without scheme.' error visible in vscode when activating the vRO extension

### Removed
* The `o11n.server.*` configuration properties for the VSCode extension are no longer used. They are replaced by the settings defined `o11n.maven.profile`
* Removed Maven-based hint collection

### Known Issues
* Cannot build project generated with groupId or artifactId that contain special characters.
    * Cause: The Jasmine tests are unable to compile if the folder hierarchy contains characters that are not allowed in Java packages.
    * Workaround: If a generated project contains special characters in its groupId or artifactId, rename all subfolders in test/ and src/ to not include any non-compatible with the Java package convention characters.

## v1.1.5 - 19 Jul 2018

### Fixes
* When trying to pull a package from vRO 7.3 with v1.1.4 of the toolchain, it reports the package is not found even though the package is there.

## v1.1.4 - 17 Jul 2018

### Enhancements
* Include empty .o11n directory in the generated vRO projects. Such projects will trigger the vRO extension activation when opened in VSCode
* Provide the ability to fetch contents from any vRO package by using `mvn vro:pull -DpackageName=com.vmware.pscoe.library.ssh`

### Fixes
* Pull does not work for vRO 7.4
* Other minor bug fixes and improvements

## v1.1.3 - 13 Jun 2018

### Enhancements
* Support pulling and pushing configuration values

### Fixes
* Installer cannot import bundle with both vRO and vRA content
* Maven-based hint collection fails for mixed project

## v1.1.2 - 23 May 2018

### Enhancements
* Support component profiles in vRA projects

## v1.1.1 - 14 May 2018

### Enhancements
* Support encrypted passwords in the active maven profile
* Include stack trace information in jasmine test failures

### Fixes
* Minor bug fixes and improvements

## v1.1.0 - 03 May 2018

### Enhancements
* Support pushing content to vRO/vRA without dependencies
* Support for bulding packages (patches) with only a subset of the project's actions.

## v1.0.2 - 18 Apr 2018

### Enhancements
* Support hint collection for dependencies present only on the local machine

### Fixes
* Log4j2 logs an error that configuration is missing when building/testing packages

## v1.0.1 - 13 Mar 2018

### Fixes
* Cloud Client could not import bundles

## v1.0.0 - 02 Mar 2018
* Initial version