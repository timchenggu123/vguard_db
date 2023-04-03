# VGuardDB: An Extension of VGuard for Efficiently Storing and Accessing Data from V2X Networks
A database for VGuard
VGuardDB is a project that extends VGuard, a permissioned blockchain designed for achieving consensus under dynamic memberships in V2X networks. VGuardDB creates a storage layer upon VGuard to make the generated data available to all users in a structured and organized way, implementing the necessary read functionalities to read the data that is stored in the ledger. As database, SQLite is used, a widely used database management system known for its reliability and efficiency.

In addition, VGuard has been extended to support messages from real-use case scenarios, specifically from on-vehicle GPS data sensors,provided from the open-source dataset PVS - Passive Vehicular Sensors Datasets(https://www.kaggle.com/datasets/jefmenegazzo/pvs-passive-vehicular-sensors-datasets?resource=download-directory). This allows users to store and retrieve data from V2X networks in a more meaningful and efficient way.

VGuardDB provides the following features:

    - Extension of VGuard to support messages from on-vehicle GPS data sensors
    - Implementation of read functionalities to read the data stored in the ledger
    - Storage layer to make the generated data available to all users in a structured and organized way
    - Usage of SQLite as the database management system

To get started with VGuardDB, please refer to the documentation provided in the repository. We welcome contributions and feedback from the community to make this project even more robust and useful for storing and accessing data from V2X networks.