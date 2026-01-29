"""MT5 client management module.

Provides a singleton client manager for maintaining MT5 connections
across multiple skill executions.
"""

from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator

from pdmt5 import Mt5Config, Mt5TradingClient

if TYPE_CHECKING:
    pass


class Mt5ClientManager:
    """Thread-safe singleton manager for MT5 client connections.

    This class ensures that only one MT5 connection is active at a time
    and provides methods for skill access to the trading client.
    """

    _instance: Mt5ClientManager | None = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> Mt5ClientManager:
        """Create or return the singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the client manager."""
        if self._initialized:
            return
        self._client: Mt5TradingClient | None = None
        self._config: Mt5Config | None = None
        self._connected: bool = False
        self._client_lock: threading.Lock = threading.Lock()
        self._initialized: bool = True

    def configure(
        self,
        login: int,
        password: str,
        server: str,
        timeout: int = 60000,
        path: str | None = None,
    ) -> None:
        """Configure the MT5 connection parameters.

        Args:
            login: MT5 account number.
            password: MT5 account password.
            server: MT5 server name.
            timeout: Connection timeout in milliseconds.
            path: Optional path to MT5 terminal executable.
        """
        self._config = Mt5Config(
            login=login,
            password=password,
            server=server,
            timeout=timeout,
            path=path,
        )

    def connect(self) -> bool:
        """Establish connection to MT5.

        Returns:
            True if connection successful, False otherwise.

        Raises:
            RuntimeError: If not configured before connecting.
        """
        if self._config is None:
            raise RuntimeError("Mt5ClientManager not configured. Call configure() first.")

        with self._client_lock:
            if self._connected and self._client is not None:
                return True

            self._client = Mt5TradingClient(config=self._config)
            try:
                self._client.initialize_and_login_mt5()
                self._connected = True
                return True
            except Exception:
                self._client = None
                self._connected = False
                raise

    def disconnect(self) -> None:
        """Disconnect from MT5."""
        with self._client_lock:
            if self._client is not None:
                try:
                    self._client.shutdown()
                except Exception:
                    pass
                finally:
                    self._client = None
                    self._connected = False

    def get_client(self) -> Mt5TradingClient:
        """Get the active MT5 trading client.

        Returns:
            The connected MT5TradingClient instance.

        Raises:
            RuntimeError: If not connected to MT5.
        """
        if not self._connected or self._client is None:
            raise RuntimeError("Not connected to MT5. Call connect() first.")
        return self._client

    @property
    def is_connected(self) -> bool:
        """Check if connected to MT5."""
        return self._connected

    @property
    def is_configured(self) -> bool:
        """Check if the manager has been configured."""
        return self._config is not None


# Global client manager instance
_client_manager: Mt5ClientManager | None = None


def get_client_manager() -> Mt5ClientManager:
    """Get the global MT5 client manager instance.

    Returns:
        The singleton Mt5ClientManager instance.
    """
    global _client_manager
    if _client_manager is None:
        _client_manager = Mt5ClientManager()
    return _client_manager


@contextmanager
def mt5_connection(
    login: int,
    password: str,
    server: str,
    timeout: int = 60000,
    path: str | None = None,
) -> Generator[Mt5TradingClient, None, None]:
    """Context manager for MT5 connections.

    Provides a convenient way to establish and automatically close
    MT5 connections.

    Args:
        login: MT5 account number.
        password: MT5 account password.
        server: MT5 server name.
        timeout: Connection timeout in milliseconds.
        path: Optional path to MT5 terminal executable.

    Yields:
        Connected Mt5TradingClient instance.

    Example:
        >>> with mt5_connection(12345, "password", "Server") as client:
        ...     account = client.account_info_as_df()
    """
    manager = get_client_manager()
    manager.configure(login, password, server, timeout, path)
    manager.connect()
    try:
        yield manager.get_client()
    finally:
        manager.disconnect()
