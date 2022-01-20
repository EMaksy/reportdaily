defmodule Tronto.Monitoring.ClusterReadModel do
  @moduledoc """
  Cluster read model
  """

  use Ecto.Schema

  import Ecto.Changeset

  @type t :: %__MODULE__{}

  @derive {Jason.Encoder, except: [:__meta__, :__struct__]}
  @primary_key {:id, :binary_id, autogenerate: false}
  schema "clusters" do
    field :name, :string
    field :sid, :string
    field :type, Ecto.Enum, values: [:hana_scale_up, :hana_scale_down, :unknown]
  end

  @spec changeset(t() | Ecto.Changeset.t(), map) :: Ecto.Changeset.t()
  def changeset(cluster, attrs) do
    cast(cluster, attrs, __MODULE__.__schema__(:fields))
  end
end
