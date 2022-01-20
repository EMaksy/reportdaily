defmodule Tronto.Monitoring.Domain.Events.HostAddedToCluster do
  @moduledoc """
    This event is emitted when a host is added to a cluster
  """

  use TypedStruct

  @derive Jason.Encoder
  typedstruct do
    @typedoc "HostAddedToCluster event"

    field :id_cluster, String.t(), enforce: true
    field :id_host, String.t(), enforce: true
  end
end
