"""Pulumi Cloud tap class."""

from __future__ import annotations

import typing as t

import requests_cache
from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_pulumi_cloud import (
    audit_logs,
    environments,
    organizations,
    policies,
    rum,
    stacks,
    webhooks,
)


class TapPulumiCloud(Tap):
    """Singer tap for Pulumi Cloud."""

    name = "tap-pulumi-cloud"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            required=True,
            description="API Token for Pulumi Cloud",
        ),
        th.Property(
            "organizations",
            th.ArrayType(th.StringType),
            description="List of organizations to sync",
            required=True,
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
        th.Property(
            "requests_cache",
            th.ObjectType(
                th.Property(
                    "enabled",
                    th.BooleanType,
                    default=False,
                    description="Enable requests cache",
                ),
                th.Property(
                    "config",
                    th.ObjectType(
                        th.Property(
                            "expire_after",
                            th.IntegerType,
                            description="Cache expiration time in seconds",
                        ),
                    ),
                    description="Requests cache configuration",
                    default={},
                ),
            ),
            description="Cache configuration for HTTP requests",
        ),
        additional_properties=False,
    ).to_dict()

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """Initialize the tap."""
        super().__init__(*args, **kwargs)

        if self.config.get("requests_cache", {}).get("enabled", False):
            requests_cache.install_cache(
                "requests_cache",
                **self.config["requests_cache"].get("config", {}),
            )

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Pulumi Cloud streams.
        """
        return [
            stacks.Stacks(tap=self),
            stacks.StackDetails(tap=self),
            stacks.StackUpdates(tap=self),
            stacks.StackResources(tap=self),
            stacks.StackPolicyGroups(tap=self),
            stacks.StackPolicyPacks(tap=self),
            stacks.StackPreviews(tap=self),
            stacks.StackDeployments(tap=self),
            stacks.StackSchedules(tap=self),
            stacks.StackScheduledDeploymentHistory(tap=self),
            organizations.OrganizationMembers(tap=self),
            organizations.OrganizationTeams(tap=self),
            organizations.OrganizationAccessTokens(tap=self),
            organizations.OrganizationTeamsMembers(tap=self),
            organizations.OrganizationTeamsStacks(tap=self),
            organizations.OrganizationTeamsEnvironments(tap=self),
            organizations.OrganizationTeamsAccessTokens(tap=self),
            organizations.OrganizationOidcIssuers(tap=self),
            organizations.OrganizationOidcIssuersPolicies(tap=self),
            organizations.OrganizationAgentPools(tap=self),
            policies.PolicyGroupsList(tap=self),
            policies.PolicyGroups(tap=self),
            policies.PolicyPacks(tap=self),
            policies.LatestPolicyPacks(tap=self),
            rum.RumUsageDaily(tap=self),
            environments.Environments(tap=self),
            webhooks.OrganizationWebhooks(tap=self),
            webhooks.OrganizationWebhookDeliveries(tap=self),
            webhooks.StackWebhooks(tap=self),
            webhooks.StackWebhookDeliveries(tap=self),
            audit_logs.AuditLogs(tap=self),
        ]
