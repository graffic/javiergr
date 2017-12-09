title: Building an standalone druid hadoop indexer
date: 2017-12-09
category: technical
published: true
summary: How to build a fat jar for command line indexing jobs in a hadoop cluster.

[Druid](http://druid.io) can do [batch data ingestion](http://druid.io/docs/latest/ingestion/batch-ingestion.html)
using hadoop and start indexing jobs [via command line](http://druid.io/docs/latest/ingestion/command-line-hadoop-indexer.html)
so you wont need an overlord/middle manager/peon. You can run those jobs using any scheduler 
or even by hand when needed (Ex: rebuild from raw data backups). Some times the issue at hand is that
druid and hadoop tend to not to be very good friends because they use some common libraries but in different versions.

## Some Context

Where I [work](https://www.glispa.com), we use Druid 0.9.2, 0.11.0 with a [Cloudera Hadoop](https://www.cloudera.com/products/open-source/apache-hadoop/key-cdh-components.html)
cluster where we schedule jobs using [airflow](http://pythonhosted.org/airflow/index.html).
We chose the *fat-jar* option so we can treat the indexers as an app to deploy and then use configuration and task
files to index different data.

The information in the [druid official documentation](http://druid.io/docs/latest/operations/other-hadoop.html)
about working with different versions of Hadoop put us on the right track.
The issue was the loading order of the different dependencies druid needs. While `io.druid.cli.Main` seemed to work in the host launching
the job, it wasn't working in the data nodes. 

If you see the following errors, this post might help.

    :::
    io.druid.java.util.common.ISE: Unknown module type[class io.druid.server.initialization.jetty.JettyServerModule]

    com.google.inject.util.Types.collectionOf(Ljava/lang/reflect/Type;)Ljava/lang/reflect/ParameterizedType
    
    com.google.common.base.Enums.getIfPresent(Ljava/lang/Class;Ljava/lang/String;)Lcom/google/common/base/Optional;
    
    java.lang.IllegalArgumentException: Invalid format: "1469433667658" is malformed at "7658"
        at org.joda.time.format.DateTimeParserBucket.doParseMillis(DateTimeParserBucket.java:187)
    
    Error: com.fasterxml.jackson.core.JsonFactory.requiresPropertyOrdering()
    
    java.lang.NoSuchMethodError: org.apache.hadoop.yarn.api.records.ContainerId.fromString

    1) A binding to javax.net.ssl.SSLContext was already configured
      at io.druid.server.emitter.HttpEmitterModule.configureSsl(HttpEmitterModule.java:70).
      at io.druid.server.emitter.HttpEmitterModule.configureSsl(HttpEmitterModule.java:70)


## Building the fat jar

You will need a system with **Oracle JDK 8** and **maven**. We're going to modify the following files:

- `pom.xml` See the changes here: 
    [0.9.2 & 0.10.1](https://gist.github.com/graffic/d911ee3fa413e73cd83cb61d97bb8486#file-0-10-1_properties_in_pom-xml),
    [0.11.0](https://gist.github.com/graffic/d911ee3fa413e73cd83cb61d97bb8486#file-0-11-0_properties_in_pom-xml).
- `TaskConfig.java`
- `sevices/pom.xml` See the final result here:
    [0.9.2 & 0.10.1](https://gist.github.com/graffic/d911ee3fa413e73cd83cb61d97bb8486#file-0-10-1_full_services_pom-xml),
    [0.11.0](https://gist.github.com/graffic/d911ee3fa413e73cd83cb61d97bb8486#file-0-11-0_full_services_pom-xml).
- `ParametrizedUriEmitterModule.java` Only for 0.11.0

Let's start downloading druid source code and opening the root pom.xml file:

- Set  `<hadoop.compile.version>` to the version of hadoop CDH needs but without cdh extensions. For CDH 5.10.2 it means 2.6.0 and not 2.6.0-cdh5.10.2 or 2.6.0-mr1-cdh5.10.1.
- Set `<guice.version>` to the one CDH hadoop is using. `3.0` for CDH 5.10.2
- While modifying the hadoop version there is a note about updating also `TaskConfig.java` here `indexing-service/src/main/java/io/druid/indexing/common/config/`

Go to the `service/` directory and open its `pom.xml`. Add the extra extensions you need in your fat jar before the `<!-- Test Dependencies -->` line. For example:

    :::xml
    <dependency>
        <groupId>io.druid.extensions</groupId>
        <artifactId>druid-avro-extensions</artifactId>
        <version>${project.parent.version}</version>
    </dependency>

    <dependency>
        <groupId>io.druid.extensions.contrib</groupId>
        <artifactId>druid-parquet-extensions</artifactId>
        <version>${project.parent.version}</version>
    </dependency>

    <dependency>
        <groupId>io.druid.extensions</groupId>
        <artifactId>druid-hdfs-storage</artifactId>
        <version>${project.parent.version}</version>
    </dependency>

    <dependency>
        <groupId>io.druid.extensions</groupId>
        <artifactId>mysql-metadata-storage</artifactId>
        <version>${project.parent.version}</version>
    </dependency>

    <dependency>
        <groupId>io.druid.extensions</groupId>
        <artifactId>druid-s3-extensions</artifactId>
        <version>${project.parent.version}</version>
    </dependency>

Now it's time to configure the maven shade plugin in the previous `pom.xml`. I found 
problems with the latest version so let's downgrade it. Find this line `<artifactId>maven-shade-plugin</artifactId>`
and add this line under it to set the version: `<version>2.4.3</version>`

The second step in the `pom.xml` is to shade **jackson** and **google.common**.
Find the `</outputs>` line and insert the following relocations for **0.9 and 0.10** only (see below for 0.11):

    :::xml
    <relocations>
        <relocation>
            <pattern>com.fasterxml.jackson</pattern>
            <shadedPattern>shade.com.fasterxml.jackson</shadedPattern>
        </relocation>
        <relocation>
            <pattern>com.google.common</pattern>
            <shadedPattern>shade.com.google.common</shadedPattern>
        </relocation>
    </relocations>

### Druid 0.11

You only need one relocation in `services/pom.xml`:

    :::xml
    <relocations>
        <relocation>
            <pattern>com.fasterxml.jackson</pattern>
            <shadedPattern>shade.com.fasterxml.jackson</shadedPattern>
        </relocation>
    </relocations>

I found an issue with SSL bindings and *Guice* comming from `server/src/main/java/io/druid/server/emitter/ParametrizedUriEmitterModule.java`. Delete the line containing `HttpEmitterModule.configureSsl(binder);` (Line 44)

### Building

Go back to the root directory of the druid source a and run: `mvn -DskipTests -pl services -am clean install` to build the fat-jar.
After the build finishes you will find it in `services/target/druid-services-0.??.?-selfcontained.jar`.

## Running an index job

You will need an `.spec` file as explained in [batch ingestion](http://druid.io/docs/latest/ingestion/batch-ingestion.html)
and [command line hadoop indexer](http://druid.io/docs/latest/ingestion/command-line-hadoop-indexer.html).

You can still put some configuration in config files, but we decided to pass it through
command line parameters. Let's see an example using s3 as deep storage.

    :::sh
    java \
    -Xmx512m \
    -Duser.timezone=UTC \
    -Dfile.encoding=UTF-8 \
    -Ddruid.storage.type=s3 \
    -Ddruid.s3.accessKey=KEY \
    -Ddruid.s3.secretKey=SECRET_KEY\
    -Ddruid.storage.bucket=myBucket \
    -cp "$(hadoop classpath):druid-service-0.11.0-selfcontained.jar" \
    io.druid.cli.Main index hadoop --no-default-hadoop task.spec

That's all! We were quite focused on building a fat jar, although
it might be easier for you to play with classpath preferences and use a normal druid build.